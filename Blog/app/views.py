from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *

from . serializers import *
from rest_framework import viewsets
from rest_framework import permissions


# Create your views here.
def index(request):
    all_obj = Article.objects.all()
    search = request.GET.get("search")
    if search:
        all_obj = all_obj.filter(Q(title__icontains=search) | Q(category__name__icontains=search))

    paginator = Paginator(all_obj, 3)  # Show 3 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'all_obj': page_obj,
    }
    return render(request, "index.html", context)


def profilePage(request, name):
    post_author = get_object_or_404(User, username=name)
    auth = get_object_or_404(Author, name=post_author)
    post = Article.objects.filter(article_author=auth)
    context = {
        'auth': auth,
        'post': post,
    }
    return render(request, "profile.html", context)


def singlePage(request, id):
    obj = get_object_or_404(Article, id=id)
    getComment = Comment.objects.filter(post=id)
    related_post = Article.objects.filter(category=obj.category).exclude(id=id)
    form = CommentFrom(request.POST)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.post = obj
        instance.save()
    context = {
        'obj': obj,
        'related_post': related_post,
        'form':form,
        'getComment':getComment,
    }
    return render(request, "single.html", context)


def Topic(request, name):
    cat = get_object_or_404(Category, name=name)
    all_obj = Article.objects.filter(category=cat)
    context = {
        'all_obj': all_obj,
    }
    return render(request, "category.html", context)


def register_request(request):
    form = RegistrationForm()
    if request.method == 'GET':
        form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations!! Registration Successfully!')
    context = {'form': form}
    return render(request, 'registration.html', context)


def Login(request):
    if request.user.is_authenticated:
        return redirect("index")
    else:
        if request.method == "POST":
            name = request.POST.get("name")
            password = request.POST.get("password")
            auth = authenticate(request, username=name, password=password)
            if auth is not None:
                login(request, auth)
                return redirect("/")
    return render(request, 'login.html')


def getLogout(request):
    logout(request)
    return redirect("index")


def PostForm(request):
    if request.user.is_authenticated:
        user = get_object_or_404(Author, name=request.user.id)
        if request.method == 'POST':
            form = CreateForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.article_author = user
                instance.save()
                return redirect('index')
        else:
            form = CreateForm()

        context = {'form': form}
        return render(request, 'form.html', context)
    else:
        return redirect('login')


def Update(request, id):
    if request.user.is_authenticated:
        user = get_object_or_404(Author, name=request.user)
        post = get_object_or_404(Article, id=id)
        form = CreateForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author = user
            instance.save()
            return redirect('profile_item')
        context = {'form': form}
        return render(request, 'form.html', context)
    else:
        return redirect('login')


def Delete(request, id):
    if request.user.is_authenticated:
        obj = Article.objects.get(id=id)
        obj.delete()
        return redirect('pro')
    else:
        return redirect('login')


def ProfileListItem(request):
    if request.user.is_authenticated:
        obj = get_object_or_404(User, id=request.user.id)
        author_profile = Author.objects.filter(name=obj.id)
        if author_profile:
            authUser = get_object_or_404(Author, name=request.user.id)
            post = Article.objects.filter(article_author=authUser.id)
            context = {
                'post': post,
                'obj': authUser
            }
            return render(request,'profile_item.html',context)
        else:
            form = AuthorFrom(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.name = obj
                instance.save()
                return redirect('profile_item')
            return render(request,'create_author.html',{'form':form})
    else:
        return redirect('login')


def CategoryList(request):
    cat = Category.objects.all()
    context = {'cat':cat}
    return render(request,'category_list.html',context)

def AddCategoryItem(request):
    if request.user.is_authenticated:
        form = CategoryAddFrom(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category')
    else:
        raise Http404("You are not authorized to access this page!")

    context = {'form':form}
    return render(request,'category_add.html', context)

# serializers view
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AutherSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]