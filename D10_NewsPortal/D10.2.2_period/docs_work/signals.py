
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *
from .tasks import task_notify_post_subscriber

#@receiver(post_save, sender=Post)
#def notify_post_subscriber(sender, instance, **kwargs):
#    print('----- notify_post_subscriber----- start')
#    tmp = PostCategory.objects.filter(post_id = instance.pk).values('category')
#    print('len query:', len(tmp))
#    if len(tmp) > 0:      
#        task_notify_post_subscriber.apply_async([instance.pk], countdown = 0)        # Вызов задачи для celery   
#    print('----- notify_post_subscriber----- finish')  
    


