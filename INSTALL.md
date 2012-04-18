# Adlibre TMS installation

## This is how we setup a development environment

# cd ( to your virtualenv base)
# mkvirtualenv --no-site-packages tms
# workon tms
# cdvirtualenv
# pip install -e git+git://github.com/macropin/Adlibre-TMS.git#egg=adlibre_tms-dev 
# ./adlibre_tms/manage.py collectstatic
# ./adlibre_tms/manage.py syncdb

Set your config options in _src/adlibre_tms/local_settings.py_.

## This is how we deploy on CentOS 5.X w/ lighttpd

# su - wwwpub
# cd /srv/www
# mkvirtualenv --no-site-packages --python /usr/bin/python2.6 tms
# workon tms
# cdvirtualenv
# pip install git+git://github.com/macropin/Adlibre-TMS.git
# ./adlibre_tms/manage.py collectstatic
# ./adlibre_tms/manage.py syncdb

Set your config options in _./adlibre_tms/local_settings.py_.

## Then we use the lighttpd config in ./deployment to setup lighttpd and manage the flup/fcgi processes

# ln -s  /srv/www/tms/deployment/lighttpd.conf /etc/lighttpd/conf.d/tms.conf

Add something like the following to the crontab for your web / fcgi user:
@reboot /srv/www/tms/deployment/manage-fcgi.sh restart settings_prod tms
