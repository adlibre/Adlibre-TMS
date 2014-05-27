# Adlibre TMS installation

There are various ways to install TMS. This method below is for a production install:

## This is how we deploy on CentOS / AMI / Fedora w/ Nginx

    yum install nginx
    chkconfig nginx on
    adduser wwwpub  # Add a user to own TMS app
    mkdir (your virtualenv base)
    chown wwwpub: (your virtualenv base)

### Install TMS

    cd ( to your virtualenv base)
    cd /srv/www
    curl --silent https://raw.githubusercontent.com/adlibre/python-bootstrap/master/bootstrap.sh | bash -s tms git+git://github.com/adlibre/Adlibre-TMS.git

### Configure your settings

    cd ( to your virtualenv base)
    mv ./local_settings.py.example ./local_settings.py # Edit as necessary
    mv ./.env.example .env # Edit as necessary

## Configure Nginx

Add the following to _/etc/nginx/conf.d/tms.conf_:

```
#
# Adlibre TMS
#

server {
    listen       80;
    server_name  _;

    keepalive_timeout 10;

    # path for static files
    root /srv/www/tms/www;

    location / {
        # checks for static file, if not found proxy to app
        try_files $uri @proxy_to_app;
    }

    location @proxy_to_app {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;

        proxy_pass   http://localhost:8000;
    }

}
```

### Initial Deployment

    cd ( to your virtualenv base)
    . bin/activate
    bureaucrat deploy

### Startup
    /srv/www/tms/bin/bureaucrat start --logpath /srv/www/tms/log/ --venv /srv/www/tms --pidpath /tmp/