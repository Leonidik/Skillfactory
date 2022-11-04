# URLs for docs_free

from django.urls import path
from .views import PostList, PostDetail, PostSearch  

urlpatterns = [
   path('',                            PostList.as_view(),   name='post_list'),
   path('<int:pk>/',                   PostDetail.as_view(), name='post_detail'),      
   path('docs_free/search/',           PostSearch.as_view(), name='post_search'),
   path('docs_free/search/<int:pk>/',  PostDetail.as_view(), name='post_detail'),   
   
]

