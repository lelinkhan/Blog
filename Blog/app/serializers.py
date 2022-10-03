from rest_framework import serializers
from .models import *


class AutherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id','name', 'profile_pic', 'about']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id','article_author','title', 'description', 'category', 'posted_on', 'updated_on', 'image']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','post','name','email','post_comment']
