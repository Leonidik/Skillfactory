
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import OneTimeCode

@receiver(post_save, sender=OneTimeCode)
def notify_post_subscriber(sender, instance, created=True, **kwargs):
    print('----- login code notification-------')
#    print('sender:', sender)
#    print('instance.pk   :', instance.pk)
#    print('instance.code :', instance.code)
#    print('instance.email:', instance.email)        

    send_code  = instance.code
    send_email = instance.email
    send_date  = instance.time_in.date()
    send_time  = instance.time_in.time().strftime("%H:%M:%S")
    send_datetime = instance.time_in

#    print('send datetime:  ', send_datetime)
#    print('send date    :  ', send_date)
#    print('send time    :  ', send_time)
#    print('==============================================')
    # Заголовок сообщения
    subject = f'Сообщение для {send_email} от проекта Доска объявлений'
    # Текст сообщения
    message = f'Ваш код доступа : {send_code}'
    # Почта, с которой будет осуществлена отправка сообщения  
    from_email ='leonid.malov2010@yandex.ru'
    # Список получателей
    recipient_list=[send_email]
        
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


