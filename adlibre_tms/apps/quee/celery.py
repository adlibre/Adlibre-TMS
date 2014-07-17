from __future__ import absolute_import

from celery import Celery

from django.conf import settings

# instantiate Celery object
celery = Celery(include=['adlibre_tms.apps.quee.tasks', ])

# import celery config file
celery.config_from_object('celeryconfig')

celery.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

if __name__ == '__main__':
    celery.start()