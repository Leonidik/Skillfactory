from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from django.urls import reverse

from .models import Post, Category, PostCategory

class PostListView(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'docs_free/post_list.html'
    context_object_name = 'post_list'
    paginate_by = 5
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'docs_free/post_detail.html'
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






