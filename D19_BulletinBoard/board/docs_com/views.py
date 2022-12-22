from django.shortcuts import render, redirect

# Create your views here.

from django.views.generic import ListView, DetailView, UpdateView
from django.urls import reverse
from .models import Post, Comment

from users.models import User
 
class ComPostListView(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'docs_com/com_post_list.html'
    context_object_name = 'com_post_list'
    paginate_by = 5
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
    
class ComPostDetailView(DetailView):
    model = Post
    template_name = 'docs_com/com_post_detail.html'
    context_object_name = 'com_post_detail'
    
    def get_context_data(self, **kwargs):
        context = super(ComPostDetailView, self).get_context_data(**kwargs)

        post_id = self.kwargs['pk']
        cat_ids = PostCategory.objects.filter(post_id=post_id)
        categories = ''
        for cat in list(cat_ids):
            cat_id = cat.category_id                    
            category = Category.objects.get(pk=cat_id).name
            categories += category+', '
        context['category'] = categories[:-2]
        return context

# ----- Comments ------

class CommentListReceivedView(ListView):
    model = Comment
    ordering = '-time_in'
    template_name = 'docs_com/comment_list_recieved.html'
    context_object_name = 'comment_list_received'
    paginate_by = 5
            
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(user=self.request.user) 
        return queryset.filter(received=True)     
                  
class CommentListAdoptedView(ListView):
    model = Comment
    ordering = '-time_in'
    template_name = 'docs_com/comment_list_adopted.html'
    context_object_name = 'comment_list_adopted'
    paginate_by = 5
            
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(user=self.request.user) 
        return queryset.filter(adopted=True)     

class CommentListRejectedView(ListView):
    model = Comment
    ordering = '-time_in'
    template_name = 'docs_com/comment_list_rejected.html'
    context_object_name = 'comment_list_rejected'
    paginate_by = 5
            
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(user=self.request.user) 
        return queryset.filter(rejected=True)  



class CommentDetailView(DetailView):
    model = Comment
    template_name = 'docs_com/comment_detail.html'
    context_object_name = 'comment_detail'
  
def adoption_item(request, pk):
    item = Comment.objects.get(pk=pk)
    item.received = False
    item.adopted  = True
    item.save()    
    return redirect('/docs_com/comment_list_received/')

def rejection_item(request, pk):
    item = Comment.objects.get(pk=pk)
    item.received = False
    item.rejected = True
    item.save()    
    return redirect('/docs_com/comment_list_received/')


#class CommentUpdateView(UpdateView):
#    form_class = CommentForm
#    model = Comment
#    template_name = 'docs_com/comment_update.html' 
    
#    def form_valid(self, form):
#        post = form.save(commit=True)
#        return super().form_valid(form)
        
#    def get_success_url(self):
#        return reverse('comment_detail',  args=[self.object.pk])        
        
        
        
        


