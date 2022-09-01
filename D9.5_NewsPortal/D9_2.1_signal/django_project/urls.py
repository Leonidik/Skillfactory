"""django_project URL Configuration
"""


from django.contrib import admin
from django.urls import path, include

urlpatterns = [
   path('admin/', admin.site.urls),
   path('users/',     include('users.urls')),
   path('accounts/',  include('allauth.urls')),  
   path('',           include('docs_free.urls')),
   path('docs_free/', include('docs_free.urls')),   
   path('docs_work/', include('docs_work.urls')),  
      
   ]
