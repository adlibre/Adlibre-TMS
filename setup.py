#!/usr/bin/env python

import os
import fnmatch

from setuptools import setup, find_packages


#def is_package(path):
#    return (
#        os.path.isdir(path) and
#        os.path.isfile(os.path.join(path, '__init__.py'))
#        )
#
#def find_packages(path, base="" ):
#    """ Find all packages in path """
#    packages = {}
#    for item in os.listdir(path):
#        dir = os.path.join(path, item)
#        if is_package( dir ):
#            if base:
#                module_name = "%(base)s.%(item)s" % vars()
#            else:
#                module_name = item
#            packages[module_name] = dir
#            packages.update(find_packages(dir, module_name))
#    return packages

def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for base_name in files:
            if fnmatch.fnmatch(base_name, pattern):
                filename = os.path.join(root, base_name)
                if os.path.isfile(filename):
                    yield filename

def findall(dir,pattern='*'):
    """
        A better finder

        Returns the full relative path to the file
    """
    all_files = []
    for root, dirs, files in os.walk(dir):
        for file in fnmatch.filter(files, pattern):
            file_path = os.path.join(root, file)
            all_files.extend((file_path,))
    return (dir, all_files)


setup(name='adlibre_tms',
    version='0.1.0',
    long_description=open('README.md').read(),
    url='https://github.com/macropin/Adlibre-TMS',
    packages=find_packages('.'),
    scripts=[],
    package_data={
            'adlibre_tms': [
                'apps/saasu_client/templates/saasu_client/*.xml',
                'apps/tms/contrib/saasu/media/admin/saasu/js/*.js',
                'apps/tms/contrib/saasu/templates/saasu/admin/*.html',
                'apps/tms/fixtures/initial_data.json',
                'apps/tms/templates/tms/*.html',
                'templates/*.html',
                'templates/admin/*.html',
                'templates/admin/tms/*.html',
                'templates/admin/tms/customer/*.html',
                'templates/admin/tms/job/*.html',
                'templates/admin/tms/project/*.html',
                'templates/admin/tms/services/*.html',
                'templates/blue_theme/*.html',
                'templates/blue_theme/adlibre/contrib/widgets/*.html',
                'templates/blue_theme/pagination/*.html',
                'templates/blue_theme/registration/*.html',
                'templates/blue_theme/reporting/*.html',
                'templates/blue_theme/tms/*.html',
                'templates/blue_theme/tms/reports/*.html',
                'templates/blue_theme/uni_form/*.html',
            ], # this should be done automatically
        },
    data_files = [
            ('adlibre_tms', ['local_settings.py', 'adlibre_tms/manage.py']),
            ('db', ['db/.gitignore']),
            ('deployment', find_files('deployment', '*')),
            ('docs', find_files('docs', '*')),
            findall('www'),
#            ('www/media/blue_theme/tms/css', ['www/media/blue_theme/tms/css/*.css']),
#            ('www/media/blue_theme/tms/images', ['www/media/blue_theme/tms/images/*']),
#            ('www/media/blue_theme/tms/js', ['www/media/blue_theme/tms/js/*.js', 'www/media/blue_theme/tms/js/*.htc']),
#            ('www/media/blue_theme/tms/js/jquery-themes/base', ['www/media/blue_theme/tms/js/jquery-themes/base/*.css']),
#            ('www/media/blue_theme/tms/js/jquery-themes/base/images', ['www/media/blue_theme/tms/js/jquery-themes/base/images/*']),
#            ('www/media/blue_theme/tms/js/jquery-themes/ui-lightness', ['www/media/blue_theme/tms/js/jquery-themes/ui-lightness/*.css']),
#            ('www/media/blue_theme/tms/js/jquery-themes/ui-lightness/images', ['www/media/blue_theme/tms/js/jquery-themes/ui-lightness/images/*']),
#            ('www/media/blue_theme/tms/js/jquery-ui', ['www/media/blue_theme/tms/js/jquery-ui/*.js']),
#            ('www/media/blue_theme/tms/js/jquery-ui/i18n', ['www/media/blue_theme/tms/js/jquery-ui/i18n/*.js']),
#            ('www/media/blue_theme/tms/js/jquery-ui/minified', ['www/media/blue_theme/tms/js/jquery-ui/minified/*.js']),
#            ('www/media/blue_theme/uni_form', ['www/media/blue_theme/uni_form/*']),
        ],
    install_requires=[
            'BeautifulSoup==3.2.0',
            'Django==1.3.1',
            'django-any==0.2.0',
            'django-compressor==1.1.1',
            'django-pagination==1.0.7',
            'django-uni-form==0.7.0',
            'flup==1.0.3.dev-20110405',
            'python-dateutil==2.0',
            'template-utils==0.4p2',
            'xml-models==0.5.1'
        ],
#    dependency_links = [
#        ],
)


print findall('www')