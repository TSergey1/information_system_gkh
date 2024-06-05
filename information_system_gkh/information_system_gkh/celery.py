import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'information_system_gkh.settings')

app = Celery('information_system_gkh')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
