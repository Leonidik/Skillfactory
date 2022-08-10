from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from .models import Post
from django.contrib.auth.models import User

from .filters import PostFilter, EditFilter

class PostList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'docs_free/post_list.html'
    context_object_name = 'post_list'
    paginate_by = 5
    
class PostSearch(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'docs_free/post_search.html'
    context_object_name = 'post_search'
    paginate_by = 5
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context     
    
class PostDetail(DetailView):
    model = Post
    template_name = 'docs_free/post_detail.html'
    context_object_name = 'post_detail'
