import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
app = Celery('django_project')
app.config_from_object('django.conf:settings', namespace = 'CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'print every weak on Monday': {
        'task': 'docs_work.tasks.task_weekly',
        'schedule'  : crontab(hour=8, minute=00, day_of_week='monday'),      
    },
}


