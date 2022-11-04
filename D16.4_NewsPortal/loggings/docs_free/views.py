from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from .models import Post, PostCategory, Category
from django.contrib.auth.models import User

from .filters import PostFilter, EditFilter

#import logging
#logger = logging.getLogger(__name__)
#print('__name__:', __name__)
#logger_django   = logging.getLogger('django')
#logger_request  = logging.getLogger('django.request')
#logger_server   = logging.getLogger('django.server')
#logger_template = logging.getLogger('django.template')
#logger_security = logging.getLogger('django.security')


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


class PostDetail(DetailView):
    model = Post
    template_name = 'docs_free/post_detail.html'
    context_object_name = 'post_detail'
        
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
#        context['is_author'] = self.request.user.groups.filter(name = 'authors').exists()

        post_id = self.kwargs['pk']
        cat_ids = PostCategory.objects.filter(post_id=post_id)
        categories = ''
        for cat in list(cat_ids):
            cat_id = cat.category_id                    
            category = Category.objects.get(pk=cat_id).name
            categories += category+', '
        context['category'] = categories[:-2]
        
#        print('----------------------------------------------------------')   
#        logger_django.info(f'{__name__} | {Post.objects.get(pk=post_id).title[:20]} .')
#        logger_django.warning(f'{__name__} | {Post.objects.get(pk=post_id).title[:20]} ..')
#        logger_django.error(f'{__name__} | {Post.objects.get(pk=post_id).title[:20]} ...')       
#        logger_django.critical(f'{__name__} | {Post.objects.get(pk=post_id).title[:20]} ....')        
#        print('----------------------------------------------------------')          
                
#        print()
#        logger_request.info(f'{__name__} | {Post.objects.get(pk=post_id).title[:20]} ...')
#        print()        
#        logger_server.info(f'{__name__} | {Post.objects.get(pk=post_id).title[:20]} ...')
#        print()                      
#        logger_template.info(f'{__name__} | {Post.objects.get(pk=post_id).title[:20]} ...') 
#        print() 
#        logger_security.info(f'{__name__} | {Post.objects.get(pk=post_id).title[:20]} ...')        
#        print('==========================================================')        
 
        return context 



    
    
    
    
