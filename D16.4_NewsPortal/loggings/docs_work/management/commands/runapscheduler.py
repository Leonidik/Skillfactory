
import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.db.models import Q
from django.core.mail import send_mail
from docs_work.models import *

import datetime
from django.utils.timezone import get_current_timezone

logger = logging.getLogger(__name__)

# Наша задача для периодического выполнения
def my_job():
    # Определение временных границ для текущего периода
    time_delta = 20    #------ срабатывание каждые 20 секунд
    dt_now = datetime.datetime.now()   
    delta  = datetime.timedelta(seconds=time_delta)
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
                        
#        send_mail(subject, message, from_email, recipient) 

    print('***************************************')
#----------------------------------------------------------------
# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    help = "Runs apscheduler."
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        # Добавляем работу нашему задачнику
        # Каждые 5 секунд будет запускаться функция "my_job"
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/20"),  #------ срабатывание каждые 20 секунд
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True, )

        logger.info("Added job 'my_job'.")
        
        # Добавляем работу нашему задачнику
        # Каждую неделю в понедельник будет запускаться функция "delete_old_job_executions"
        # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.        
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"             ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True, )

        logger.info("Added weekly job: 'delete_old_job_executions'." )
        
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")



