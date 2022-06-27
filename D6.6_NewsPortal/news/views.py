from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from .models import Post, Author

class PostsList(ListView):
    model = Post
    ordering = 'time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    
class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'    
    
    
