# django_project URL Configuration

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',           include('docs_free.urls')), 
    path('users/',     include('users.urls')),    
    path('docs_work/', include('docs_work.urls')),   
    path('docs_com/',  include('docs_com.urls')),         
    path('ckeditor/',  include('ckeditor_uploader.urls')),      
       
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



