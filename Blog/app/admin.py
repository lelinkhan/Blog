from django.contrib import admin
from .models import *


# Register your models here.
class AuthorModel(admin.ModelAdmin):
    list_display = ['__str__']
    search_fields = ('name__username',)

    class Meta:
        model = Author
admin.site.register(Author, AuthorModel)


class CategoryModel(admin.ModelAdmin):
    search_fields = ('name',)
    list_per_page = 10

    class Meta:
        model = Category
admin.site.register(Category, CategoryModel)

class ArticleModel(admin.ModelAdmin):
    list_display = ['__str__', 'posted_on','category']
    search_fields = ('title',)
    list_filter = ['posted_on','category']
    list_per_page = 10

    class Meta:
        model = Article
admin.site.register(Article,ArticleModel)

class CommentModel(admin.ModelAdmin):
    class Meta:
        model = Comment
admin.site.register(Comment,CommentModel)
