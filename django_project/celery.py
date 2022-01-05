import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

app = Celery('django_project')
app.conf.task_track_started = True
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule={
    'every-15-seconds':{
        'task':'thumbnailer.tasks.send_email_task',
        'schedule':15,
        'args':('kamaldhiman2010@gmail.com')
    }
}
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request:{0!r}'.format(self.request))