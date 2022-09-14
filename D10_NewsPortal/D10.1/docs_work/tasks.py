from celery import shared_task
from django.core.mail import send_mail
from django.db.models import Q

from .models import *
import datetime

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

#--------------------------------------------------------------------------------------------        

@shared_task
def task_weekly():
    # Определение временных границ для текущего периода
    time_delta = 7    #------ срабатывание каждую неделю --- Должно быть согласовано с расписанием в celery
    dt_now = datetime.datetime.now()   
    delta  = datetime.timedelta(days=time_delta)
    dt_start = dt_now - delta       
    print(dt_start,'|', dt_now)
    # Получение выборки новостей, опубликованных за заданный период времени
    post_list = Post.objects.filter(
                Q(kind='NEW') & Q(time_in__gte=dt_start) & Q(time_in__lte=dt_now))                
    # Получение перечня подписчиков, подписанных на новости, опубликованных за заданный период времени
    # состав записи: подписчик - новость,
    # где возможно наличие нескольких строк с одним подписчиком, но c разными новостями
    sub_list  = Subscriber.objects.all()
    sub_post_list = []
    for sub in sub_list:
        sub_cats = Subscriber.objects.get(pk=sub.pk).category.all()
        if len(sub_cats) != 0:
            for post in post_list:
                post_cats = Post.objects.get(pk=post.pk).category.all()
                if len(post_cats) != 0:
                # Выявление ситуаций, когда пересечение множеств категорий подписчика и категорий новости,
                # опубликованой за текущий период, является не пустым, то есть, когда
                # конкретная пара подписчик-новость имеют общие категории                
                    if (len(set(sub_cats) & set(post_cats))) != 0:
                        sub_post_list.append([sub, post])
    # Составление списка 'уникальных' подписчиков
    subs = []
    for sub, post in sub_post_list:
        subs.append(sub)
    subs = set(subs)
    # Приведение вышеупомянутого перечня к виду: подписчик - [новость1, новость2, ...]
    sub_list_post = []
    for x in subs:
        posts = []
        for sub, post in sub_post_list:
            if x==sub: posts.append(post)
        sub_list_post.append([x, posts])
          
    # Подготовка данных для рассылки сообщений и их рассылка в цикле по 'уникальным' подписчикам
    subject    = 'Добрый день'
    from_email = 'leonid.malov2010@yandex.ru'
       
    for sub, posts in sub_list_post:
        message = f'Уважаемый {sub.subscriber.first_name} {sub.subscriber.last_name} !\n'+\
                  f'По Вашей подписке на новости в период с '\
                  f'{dt_start.strftime("%Y-%m-%d %H:%m:%S")} по '\
                  f'{dt_now.strftime("%Y-%m-%d %H:%m:%S")}\n'\
                  f'появились нижеследующие документы:\n\n'
        message_list = ''         
        for post in posts:
            message_list += f'* {post.time_in.strftime("%Y-%m-%d | %H:%m:%S")} | '+\
                            f'http://127.0.0.1:8000/docs_free/{post.pk}/ |\n  '+\
                            f'{post.title}\n\n'                       
        message = (message + message_list)
        recipient = [sub.subscriber.email]       
        print('-------------------------------------------------------')    
        print(message) 
        print(recipient)
                        
        send_mail(subject, message, from_email, recipient) 

    print('***************************************')








