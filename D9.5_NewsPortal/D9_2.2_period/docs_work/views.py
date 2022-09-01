from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

#---------------------------------------------------------------------------------------
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group

from .filters import PostFilter, EditFilter
from .forms   import PostForm, NewsForm, ArticleForm, SubscriberForm

from django.core.mail import send_mail
from datetime import datetime

from .models import *

#from django.db.models.signals import post_save
#from django.db.models.signals import m2m_changed
#from django.dispatch import receiver

class PostList(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'docs_work/post_list.html'
    context_object_name = 'post_list'
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name = 'authors').exists() 
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
        context['is_author'] = self.request.user.groups.filter(name = 'authors').exists() 
        return context     
    
class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'docs_work/post_detail.html'
    context_object_name = 'post_detail'
        
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name = 'authors').exists()

        post_id = self.kwargs['pk']
        cat_ids = PostCategory.objects.filter(post_id=post_id)
        categories = ''
        for cat in list(cat_ids):
            cat_id = cat.category_id                    
            category = Category.objects.get(pk=cat_id).name
            categories += category+', '
        context['category'] = categories[:-2]
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
        context['is_author'] = self.request.user.groups.filter(name = 'authors').exists()        
        return context               

# Создание =============================================================================      
class NewsCreate(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'docs_work/news_create.html' 
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.kind    = 'NEW'
        post.time_in = datetime.now()       
        user         = self.request.user  # текущий зарегистрированный пользователь, который создает документ    
        post.author  = Author.objects.get(pk=user.pk)
        # Вышеприведенных значений достаточно для доопределения модельной формы NewsForm и сохранения новости       
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['is_author'] = self.request.user.groups.filter(name = 'authors').exists()       
               
        return context  
#========================================================================================                    
class ArticleCreate(LoginRequiredMixin, CreateView):
    form_class = ArticleForm
    model = Post
    template_name = 'docs_work/article_create.html'  

    def form_valid(self, form):     
        post = form.save(commit=False)
        post.kind    = 'ART'
        post.time_in = datetime.now() 
        user         = self.request.user
        author       = Author.objects.get(pk=user.pk)    
        post.author  = author           
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['is_author'] = self.request.user.groups.filter(name = 'authors').exists()        
        return context  
            
# Обновление
class NewsUpdate(LoginRequiredMixin, UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'docs_work/news_update.html' 
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.kind    = 'NEW'
        post.time_in = datetime.now() 
        user         = self.request.user
        author       = Author.objects.get(pk=user.pk)    
        post.author  = author 
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
        post.kind    = 'ART'
        post.time_in = datetime.now() 
        user         = self.request.user
        author       = Author.objects.get(pk=user.pk)    
        post.author  = author 
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['is_author'] = self.request.user.groups.filter(name = 'authors').exists()        
        return context 

# Удаление  
class NewsDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'docs_work/news_delete.html'
    success_url = reverse_lazy('news_edit')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['is_author'] = self.request.user.groups.filter(name = 'authors').exists()        
        return context 

class ArticleDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'docs_work/article_delete.html' 
    success_url = reverse_lazy('article_edit')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['is_author'] = self.request.user.groups.filter(name = 'authors').exists()        
        return context 

#-------------- Создание подписки -----------------
@login_required
def subscribe_me(request):
    user = request.user
    try:
        sub = Subscriber.objects.get(subscriber=user)
    except:
        sub = Subscriber.objects.create(subscriber=user) 
    tmp = '/docs_work/'+str(sub.pk)+'/subscription'
    return redirect(tmp)

class SubscriberUpdate(LoginRequiredMixin, UpdateView):
    form_class = SubscriberForm
    model = Subscriber
    template_name = 'docs_work/subscriber_update.html' 
    
    def form_valid(self, form):
        return super().form_valid(form)



