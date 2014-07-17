# config file for Celery Daemon

# default RabbitMQ backend
CELERY_RESULT_BACKEND = 'amqp://'

# Celery settings:

BROKER_URL = 'amqp://guest:guest@localhost//'

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_TIMEZONE = 'Europe/Kiev'

from datetime import timedelta

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERYBEAT_SCHEDULE = {
    'calculate_time-every-30-seconds': {
        'task': 'adlibre_tms.apps.quee.tasks.calculate_retainer',
        'schedule': timedelta(seconds=30),
        'args': (16, 16)
    },
}
