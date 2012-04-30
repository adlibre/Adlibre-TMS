# AC: 2012-04-30 This file is out of date, and not maintained. Caution advised, or use lighttpd

# django.wsgi is configured to live in projects/tms/deployment.

import os
import sys
import site

# redirect sys.stdout to sys.stderr for bad libraries like geopy that uses
# print statements for optional import exceptions.
sys.stdout = sys.stderr

from os.path import abspath, dirname, join
from site import addsitedir

sys.path.insert(0, abspath(join(dirname(__file__), "../../")))

# the site module has a handy function addsitedir, which not only adds
# the directory to the pythonpath, but also processes any .pth files it finds
site.addsitedir(join(abspath(join(dirname(__file__), "../../env")), "lib/python2.6/site-packages/"))

from django.conf import settings
os.environ["DJANGO_SETTINGS_MODULE"] = "adlibre_tms.%(settings)s"

sys.path.insert(0, join(settings.PROJECT_ROOT, "apps"))

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
