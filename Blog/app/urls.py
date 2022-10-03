from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'Author', views.AuthorViewSet)
router.register(r'Category', views.CategoryViewSet)
router.register(r'Article', views.ArticleViewSet)
router.register(r'Comment', views.CommentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('', views.index, name='index'),
    path('author_profile/<name>/', views.profilePage, name='author_profile'),
    path('single_article/<int:id>/', views.singlePage, name='single_article'),
    path('topic/<name>/', views.Topic, name='topic'),
    path('login/', views.Login, name='login'),
    path('logout/', views.getLogout, name='logout'),
    path('form/', views.PostForm, name='form'),
    path('profile_item/', views.ProfileListItem, name='profile_item'),
    path('update/<int:id>/', views.Update, name='update'),
    path('delete/<int:id>/', views.Delete, name='delete'),
    path("register/", views.register_request, name="register"),
    path("All_category/", views.CategoryList, name="category"),
    path('category_add/', views.AddCategoryItem, name='category_add'),
]
