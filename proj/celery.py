from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from demoapp.tasks import add

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

app = Celery('proj')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    print("Attempting to print add.s()")
    print(add.s(2,2))
    print("Printed add.s()")

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
