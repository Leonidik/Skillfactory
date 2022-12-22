from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth import get_user_model
from .managers import CustomUserManager
from django.utils import timezone
from django.contrib.auth import get_user_model

from datetime import datetime

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email

User = get_user_model()

class OneTimeCode((models.Model)):
    time_in = time_in = models.DateTimeField(auto_now_add = True)
    email   = models.CharField(max_length = 255)
    code    = models.CharField(max_length = 255)




