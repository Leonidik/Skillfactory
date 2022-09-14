import os
from celery import Celery

#from .tasks import task_weekly

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
app = Celery('django_project')
app.config_from_object('django.conf:settings', namespace = 'CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'print every 1 minute': {
        'task': 'docs_work.tasks.task_weekly',
        'schedule'  : 60,
    },
}


