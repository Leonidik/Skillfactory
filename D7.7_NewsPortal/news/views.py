from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post
from django.contrib.auth.models import User
from .models import Author

from .filters import PostFilter, EditFilter
from .forms import PostForm, NewsForm, ArticleForm

class PostList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'post_list.html'
    context_object_name = 'post_list'
    paginate_by = 5
    
class PostSearch(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'post_search.html'
    context_object_name = 'post_search'
    paginate_by = 5
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context     
    
class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post_detail'

# Редактирование
class NewsEdit(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'news_edit.html'
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
      
class ArticleEdit(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'article_edit.html'
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

# Создание
class NewsCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html' 
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.kind = 'NEW'
        return super().form_valid(form)
                    
class ArticleCreate(CreateView):
    form_class = ArticleForm
    model = Post
    template_name = 'article_create.html'  

    def form_valid(self, form):
        post = form.save(commit=False)
        post.kind = 'ART'
        return super().form_valid(form)
            
# Обновление
class NewsUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_update.html' 
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.kind = 'NEW'
        return super().form_valid(form)
                    
class ArticleUpdate(UpdateView):
    form_class = ArticleForm
    model = Post
    template_name = 'article_update.html'  

    def form_valid(self, form):
        post = form.save(commit=False)
        post.kind = 'ART'
        return super().form_valid(form)

# Удаление  
class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_edit')

class ArticleDelete(DeleteView):
    model = Post
    template_name = 'article_delete.html' 
    success_url = reverse_lazy('article_edit')




  




    
    
