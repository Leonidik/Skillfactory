from django_filters import FilterSet, DateFilter
from .models import Post

class PostFilter(FilterSet):
   class Meta:
       model = Post
       time_in = DateFilter(field_name='time_in', attrs={'type': 'date'},)       
       fields = {
           'kind' :   ['exact'],          
           'title':   ['icontains'],
           'author__user__last_name':  ['icontains'],          
           'time_in': ['date__gt'], }
  
class EditFilter(FilterSet):
   class Meta:
       model = Post
       quertset = Post.objects.filter(kind='NEW')
       time_in = DateFilter(field_name='time_in', attrs={'type': 'date'},)   
       fields = {
           'title':   ['icontains'],
           'author__user__last_name':  ['icontains'],           
           'time_in': ['date__gt'], }
           
      
