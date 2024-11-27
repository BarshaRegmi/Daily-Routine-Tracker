from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tracker.settings')

app = Celery('Tracker')


app.conf.update(
    timezone = 'Asia/kathmandu'
)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'print-every-30-seconds': {
        'task': 'app.tasks.your_midnight_task',
        'schedule': crontab(hour = 23, minute = 59),
        
    },
}



# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
