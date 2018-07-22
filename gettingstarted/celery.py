import os
from celery import Celery

# Setting the Default Django settings module
from gettingstarted import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gettingstarted.settings')
app = Celery('gettingstarted')

# Using a String here means the worker will always find the configuration information



@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
