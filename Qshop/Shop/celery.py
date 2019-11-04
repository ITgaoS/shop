from  __future__ import absolute_import,unicode_literals
from  django.conf import settings
from celery import Celery
import os
os.environ.setdefault("DJANGO_SETTING_MODULE","CeleryTask.settings")
app=Celery("Project")
app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda :settings.INSTALLED_APPS)