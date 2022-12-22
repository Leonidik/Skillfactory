
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView,  DeleteView
from django.views.generic.edit import CreateView, UpdateView
from django.core.mail import send_mail
from django.urls import reverse

import requests
from django.shortcuts import get_object_or_404

from docs_work.models import Post, Category, PostCategory, Comment
from users.models import User
from .forms import PostForm, CommentForm
 
class PostListView(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'docs_work/post_list.html'
    context_object_name = 'post_list'
    paginate_by = 5
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'docs_work/post_detail.html'
    context_object_name = 'post_detail'
    
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)

        post_id = self.kwargs['pk']
        cat_ids = PostCategory.objects.filter(post_id=post_id)
        categories = ''
        for cat in list(cat_ids):
            cat_id = cat.category_id                    
            category = Category.objects.get(pk=cat_id).name
            categories += category+', '
        context['category'] = categories[:-2]
        return context 

class PostCreateView(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'docs_work/post_create.html' 
    
    def form_valid(self, form):  
        post = form.save(commit=False)
        post.user = self.request.user  # текущий зарегистрированный пользователь, который создает документ 
        print('---', 	post.user, post.user_id, post.user.is_authenticated) 
        post.save()    
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail',  args=[self.object.pk])
              
class PostUpdateView(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'docs_work/post_update.html' 
    
    def form_valid(self, form):
        post = form.save(commit=True)
        return super().form_valid(form)
        
    def get_success_url(self):
        return reverse('post_detail',  args=[self.object.pk])

class CommentCreateView(CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'docs_work/comment_create.html' 

    def form_valid(self, form):  
        new_comment = form.save(commit=False)       
        tmp = self.request.get_full_path()
        new_comment.post_id = tmp.split('/')[3]
        new_comment.user_id = self.request.user.pk       
#        new_comment.save()    
        return super().form_valid(form)

    def get_success_url(self):              
        return reverse('post_detail',  args=[self.object.post_id])








      
