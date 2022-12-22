
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import *
#import os

#docs_work_dir = os.getcwd()
#print('os.path:', docs_work_dir)


@receiver(post_save, sender=Comment)
def notify_post_subscriber(sender, instance, created=True, **kwargs):
    print('----- notify_post_subscriber----- start')
#    print('sender:', sender)
#    print('comment.pk     :', instance.pk)
#    print('comment.post_id:', instance.post_id)
#    print('comment.user_id:', instance.user_id)        

    post   = Post.objects.get(pk=instance.post_id)
    email_sender   = User.objects.get(pk=instance.user_id)
    email_receiver = User.objects.get(pk=post.user_id).email
        
#    print('post title    :', post)
#    print('email_sender  :', email_sender)
#    print('email_receiver:', email_receiver)

    post_date = post.time_in.date()
    post_time = post.time_in.time().strftime("%H:%M:%S")
        
    time_in  = Comment.objects.filter(post_id=post.pk, user_id=email_sender.pk).last().time_in
    comment_date = time_in.date()
    comment_time = time_in.time().strftime("%H:%M:%S")

#    print('post_datetime ', post.time_in)
#    print('email date    ', comment_date)
#    print('email time    ', comment_time)
    print('==============================================')
    # Заголовок сообщения (кому, время)
    subject = f'{comment_date} {comment_time} | Сообщение от проекта Доска объявлений'
    # Текст сообщения
    message = f'Уважаемый {email_receiver}\n \
Сообщаем Вам, что на Ваше объявление номер {post.pk} от {post_date} | {post_time}\n \
нам поступил отклик от пользователя {email_sender.email}'
    # Почта, с которой будет осуществлена отправка сообщения  
    from_email ='leonid.malov2010@yandex.ru'
    # Список получателей
    recipient_list=[email_receiver]
        
    print('subject:\n', subject)        
    print('message:\n', message)
    print('from_email:\n', from_email)
    print('recipient_list:\n', recipient_list) 
    print('==============================================')        

    # отправляем письмо
#    send_mail( 
#        subject=subject,
#        message=message, 
#        from_email = from_email,
#        recipient_list=recipient_list        


