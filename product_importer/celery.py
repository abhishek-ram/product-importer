import os
from celery import Celery
from dotenv import load_dotenv, find_dotenv

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'product_importer.settings')
load_dotenv(find_dotenv())

app = Celery('product_importer',
             broker=os.environ.get("REDIS_URL", 'redis://localhost:6379/0'))

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


# Load task modules from all registered Django app configs.
app.autodiscover_tasks()




