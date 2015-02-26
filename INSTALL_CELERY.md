#### RabbitMQ run commands for development:

RabbitMQ is a qee required for TMS Celery app to handle tasks.

Install:

    brew install rabbitmq

To have launchd start rabbitmq at login:

    ln -sfv /usr/local/opt/rabbitmq/*.plist ~/Library/LaunchAgents

Then to load rabbitmq now:

    launchctl load ~/Library/LaunchAgents/homebrew.mxcl.rabbitmq.plist

Or, if you don't want/need launchctl, you can just run:

    rabbitmq-server

#### Celerybeat service (For periodic tasks)

In the virtual env root (where manage.py resides) execute

    celery -A adlibre_tms.apps.quee.celery beat --loglevel=DEBUG

This will start the celery beat service and execute periodic tasks. 