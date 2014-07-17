# Adlibre TMS installation

## This is how we setup a development environment

    cd ( to your virtualenv base)
    mkvirtualenv --no-site-packages tms
    workon tms
    cdvirtualenv
    pip install -e git+git://github.com/adlibre/Adlibre-TMS.git#egg=tms
    cp ./src/tms/local_settings.py.example ./src/tms/adlibre_tms/local_settings.py # Edit settings as necessary
    ./src/tms/adlibre_tms/manage.py collectstatic
    ./src/tms/adlibre_tms/manage.py syncdb

Set your config options in _./src/tms/adlibre_tms/local_settings.py_.

## This is how we deploy on CentOS 5.X w/ lighttpd

    su - wwwpub
    cd /srv/www
    mkvirtualenv --no-site-packages --python /usr/bin/python2.6 tms
    workon tms
    cdvirtualenv
    pip install git+git://github.com/adlibre/Adlibre-TMS.git
    mv ./adlibre_tms/local_settings.py.example ./adlibre_tms/local_settings.py # Edit as necessary
    ./adlibre_tms/manage.py collectstatic --settings=settings_prod
    ./adlibre_tms/manage.py syncdb --settings=settings_prod

Set your config options in _./adlibre_tms/local_settings.py_.

### Then we use the lighttpd config in ./deployment to setup lighttpd and manage the flup/fcgi processes

    cp  /srv/www/tms/deployment/lighttpd.conf /etc/lighttpd/conf.d/tms.conf

Then edit _/etc/lighttpd/conf.d/tms.conf_ as necessary to suit your requirements.

Add something like the following to the crontab for your web / fcgi user:

    @reboot /srv/www/tms/deployment/manage-fcgi.sh restart settings_prod tms

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