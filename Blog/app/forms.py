from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Article,Author,Comment,Category


class CreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'description', 'category', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='Enter Username', min_length=3, max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Enter email', required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Enter Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AuthorFrom(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['profile_pic','about']


class CommentFrom(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','email','post_comment']

class CategoryAddFrom(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']