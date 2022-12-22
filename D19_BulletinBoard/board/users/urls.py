# users URLS

from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView, auth_user_view,  login_user_view

urlpatterns = [
    path('auth/',  auth_user_view,  name='auth' ),
    path('login/', login_user_view, name='login' ),

    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('logup/',  BaseRegisterView.as_view(template_name='users/logup.html'), name='logup'),
]






