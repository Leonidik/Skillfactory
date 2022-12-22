

from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, CommentCreateView

urlpatterns = [ 
   path('',          PostListView.as_view(),   name='post_list'),  
   path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
   
   path('post_create/',          PostCreateView.as_view(), name='post_create'),
   path('post_update/<int:pk>/', PostUpdateView.as_view(), name='post_update'), 
      
   path('comment_create/<int:pk>/',  CommentCreateView.as_view(), name='comment_create'),
 
] 


