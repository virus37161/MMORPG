import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_post_week': {
        'task': 'game.tasks.send_week',
        'schedule': crontab(day_of_week='monday', minute=0, hour = 8),
    },
}