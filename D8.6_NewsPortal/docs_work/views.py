from django.shortcuts import render

# Create your views here.



from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from .models import User


#---------------------------------------------------------------------------------------
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .filters import PostFilter, EditFilter
from .forms import PostForm, NewsForm, ArticleForm

class PostList(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'docs_work/post_list.html'
    context_object_name = 'post_list'
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name = 'authors').exists()
        context['is_common'] = self.request.user.groups.filter(name = 'common').exists()     #     
        return context   
      
class PostSearch(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'docs_work/post_search.html'
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
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name = 'authors').exists()
        return context       
    
class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'docs_work/post_detail.html'
    context_object_name = 'post_detail'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name = 'authors').exists()
        return context

# Редактирование
class NewsEdit(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'docs_work/news_edit.html'
    context_object_name = 'news_edit'
#    paginate_by = 5   
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = EditFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name = 'authors').exists()
        return context      
      
class ArticleEdit(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'docs_work/article_edit.html'
    context_object_name = 'article_edit'
#    paginate_by = 5   
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = EditFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name = 'authors').exists()
        return context     

# Создание
class NewsCreate(LoginRequiredMixin, CreateView):
#class NewsCreate(PermissionRequiredMixin, CreateView):
#    permission_required = ('docs_news.delete.post',
#                           'docs_news.view.post',
#                           'docs_news.add.post',
#                           'docs_news.change.post',)
    form_class = NewsForm
    model = Post
    template_name = 'docs_work/news_create.html' 
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.kind = 'NEW'
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name = 'authors').exists()
        return context
                    
class ArticleCreate(LoginRequiredMixin, CreateView):
#class ArticleCreate(PermissionRequiredMixin, CreateView):
#    permission_required = ('docs_news.delete.post',
#                           'docs_news.view.post',
#                           'docs_news.create.post',
#                           'docs_news.change.post',)
    form_class = ArticleForm
    model = Post
    template_name = 'docs_work/article_create.html'  

    def form_valid(self, form):
        post = form.save(commit=False)
        post.kind = 'ART'
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name = 'authors').exists()
        return context
            
# Обновление
class NewsUpdate(LoginRequiredMixin, UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'docs_work/news_update.html' 
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.kind = 'NEW'
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name = 'authors').exists()
        return context
                    
class ArticleUpdate(LoginRequiredMixin, UpdateView):
    form_class = ArticleForm
    model = Post
    template_name = 'docs_work/article_update.html'  

    def form_valid(self, form):
        post = form.save(commit=False)
        post.kind = 'ART'
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name = 'authors').exists()
        return context

# Удаление  
class NewsDelete(PermissionRequiredMixin, DeleteView):
#    permission_required = 'auth.change_user'
    permission_required = ('docs_news.delete.post',
                           'docs_news.view.post',
                           'docs_news.add.post',
                           'docs_news.change.post',)
    model = Post
    template_name = 'docs_work/news_delete.html'
    success_url = reverse_lazy('news_edit')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name = 'authors').exists()
        return context

class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('docs_news.delete.post',
                           'docs_news.view.post',
                           'docs_news.add.post',
                           'docs_news.change.post',)
    model = Post
    template_name = 'docs_work/article_delete.html' 
    success_url = reverse_lazy('article_edit')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name = 'authors').exists()
        return context
        
        
        

