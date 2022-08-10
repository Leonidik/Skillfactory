from django import forms
from .models import Post, Author, Category
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = ['kind','title','text','post_rating','author','category']
       
class NewsForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = ['title','text','post_rating','author','category',]                   
       
class ArticleForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = ['title','text','post_rating','author','category',]       
       
       
