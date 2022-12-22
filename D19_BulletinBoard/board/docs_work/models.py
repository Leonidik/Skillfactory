from django.db import models

# Create your models here.
from django.conf import settings

#from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from datetime import datetime

from users.models import User

class Category(models.Model):
    name  = models.CharField(max_length = 255, unique=True)
        
    def __str__(self):
        return f'{self.name}'

class Post(models.Model):
    time_in = models.DateTimeField(auto_now_add = True)
    user    = models.ForeignKey(User, on_delete = models.CASCADE, blank=True, null=True)
    title   = models.CharField(max_length = 255)
    body    = RichTextUploadingField(blank=True)

    category = models.ManyToManyField(Category, through = 'PostCategory')

    def __str__(self):
        return f'{self.title}'

class PostCategory(models.Model):
    post     = models.ForeignKey(Post,     on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    
    def __str__(self):
        return f'{self.post.pk} : {self.category.pk} | {self.category}'

class CommentStatus(models.Model):
    name =  models.CharField(max_length = 255, unique=True)
    
    def __str__(self):
        return f'{self.name}'
        
class CommentTone(models.Model):
    name =  models.CharField(max_length = 255, unique=True)
    
    def __str__(self):
        return f'{self.name}'
        
class Comment(models.Model):
    time_in = models.DateTimeField(auto_now_add = True)
    text    = models.TextField()
    
    post   = models.ForeignKey(Post,          on_delete = models.CASCADE)
    user   = models.ForeignKey(User,          on_delete = models.CASCADE)
#    status = models.ForeignKey(CommentStatus, on_delete = models.CASCADE, default=1)
#    tone   = models.ForeignKey(CommentTone,   on_delete = models.CASCADE, default=2)
    received = models.BooleanField(default=True)
    adopted  = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)


      
