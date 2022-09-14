from celery import shared_task
from django.core.mail import send_mail

from .models import *

@shared_task
def task_notify_post_subscriber(pk):
    print('******* tasks: notify_post_subscriber----- start')
    print('pk:', pk)
    post = Post.objects.get(pk=pk)
     
    # Получение QuerySet_PostCategory для сохраняемой новости
    tmp = PostCategory.objects.filter(post_id = pk).values('category')  

    # Составление списка pk категорий сохраняемой новости        
    cat_list = []
    for cat in tmp:
        cat_list.append(cat['category'])
    print('cat list:', cat_list)

    # Преобразование списка pk категорий сохнаняемой новости в строку и
    # выявление QuerySet пользователей, которые подписались на данные категории        
    cats = ''
    query = []
    for cat in cat_list:
        tmp = Category.objects.get(pk=int(cat)).name
        cats += tmp+', '
        uu = Subscriber.objects.filter(category__name=tmp)
        for u in uu:
            query.append([tmp,u.subscriber])  

    # Преобразование QuerySet пользователей в список
    sub_short_list = []
    for cat, sub in query:
        sub_short_list.append(sub)             
    sub_short_list = list(set(sub_short_list))
        
    # Cоставление списка подписчиков с указанием тех категорий сохраняемой новости,
    # на которые они (подписчики)  подписаны
    message_list = []
    for u in sub_short_list:
        cat_list = ''
        for cc, uu in query:
            if u==uu:
                cat_list += cc+', '
        message_list.append([u, cat_list])            

    # Заполнение атрибутов для отправки писем (subject, message, recipient)
    subject=f'{post.kind} : { post.time_in.strftime("%Y-%m-%d  %H:%m:%S") }'
    for person, cats in message_list:
        message = f'Уважаемый {person.first_name} {person.last_name}\n'+\
                  f'По вашей подписке на новости в категориях "{cats[:-2]}" '\
                  f'появилось новое сообщение:\n{post.title}\n\n'+\
                  f'Вы можете посмотреть данное сообщение по ссылке\n'+\
                  f'http://127.0.0.1:8000/docs_free/{post.pk}/'                      
                                             
        recipient = person.email
        print('message:')
        print(message)
        print()
        print('получатель:')
        print(recipient)
        print('........................................')

        send_mail( 
            subject=subject, 
            message=message,  
            from_email='leonid.malov2010@yandex.ru',
            recipient_list=[recipient]  ) 
    print('******* tasks: notify_post_subscriber----- finish')  
        


