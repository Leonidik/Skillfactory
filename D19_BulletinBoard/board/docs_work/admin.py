from django.contrib import admin

# Register your models here.
from .models import *
from users.models import User 

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(CommentStatus)
admin.site.register(CommentTone)
admin.site.register(Comment)





