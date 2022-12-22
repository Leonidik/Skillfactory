
from django.urls import path
from .views import ComPostListView, ComPostDetailView, CommentDetailView 
from .views import CommentListReceivedView, CommentListAdoptedView, CommentListRejectedView
from .views import adoption_item, rejection_item

urlpatterns = [ 
   path('',          ComPostListView.as_view(),   name='com_post_list'),  
   path('<int:pk>/', ComPostDetailView.as_view(), name='com_post_detail'),
        
   path('comment_list_received/',  CommentListReceivedView.as_view(), name='comment_list_received'),
   path('comment_list_adopted/',   CommentListAdoptedView.as_view(),  name='comment_list_adopted'),   
   path('comment_list_rejected/',  CommentListRejectedView.as_view(), name='comment_list_rejected'),
   
   path('adoption_item/<int:pk>/',  adoption_item,  name='adoption_item'),   
   path('rejection_item/<int:pk>/', rejection_item, name='rejection_item'),
         
   path('comment_detail/<int:pk>/',  CommentDetailView.as_view(), name='comment_detail'),
#   path('comment_update/<int:pk>/',  CommentUpdateView.as_view(), name='comment_update'),

] 


