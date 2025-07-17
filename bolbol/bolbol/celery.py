import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bolbol.bolbol.settings')

app = Celery('bolbol')

app.config_from_object(f'django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()