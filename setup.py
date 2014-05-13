#!/usr/bin/env python

import os
import fnmatch

from setuptools import setup, find_packages

from pip.req import parse_requirements

import adlibre_tms.__version__ as VERSION


install_reqs = parse_requirements('requirements.txt')
requirements = [str(ir.req) for ir in install_reqs]


def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for base_name in files:
            if fnmatch.fnmatch(base_name, pattern):
                filename = os.path.join(root, base_name)
                if os.path.isfile(filename):
                    yield filename


def find_files_full(dir, pattern='*'):
    """
    Returns a dict with full relative path to files
    """
    all_files = []
    for root, dirs, files in os.walk(dir):
        if len(files) > 0:
            for file in fnmatch.filter(files, pattern):
                file_path = os.path.join(root, file)
                all_files.extend((file_path,))
    return all_files


def findall(dir, pattern='*'):
    """
    A better finder for 'data_files'
    """
    all_files = []
    for root, dirs, files in os.walk(dir):
        if len(files) > 0:
            file_list = []
            for file in fnmatch.filter(files, pattern):
                file_path = os.path.join(root, file)
                file_list.extend((file_path,))
            all_files.extend(((root, file_list,),))
    return all_files


setup(name='adlibre_tms',
    version=VERSION,
    long_description=open('README.md').read(),
    url='https://github.com/adlibre/Adlibre-TMS',
    packages=find_packages('.'),
    scripts=[],
    package_data={
            'adlibre_tms': [
                'apps/saasu_client/templates/saasu_client/*.xml',
                'apps/tms/contrib/saasu/media/admin/saasu/js/*.js',
                'apps/tms/contrib/saasu/templates/saasu/admin/*.html',
                'apps/tms/fixtures/initial_data.json',
                'apps/tms/templates/tms/*.html',
                'apps/tms/static/tms/css/*.css',
                'apps/tms/static/tms/images/*',
                'apps/tms/static/tms/js/*.js',
                'apps/tms/static/tms/js/*.htc',
                'apps/tms/static/tms/js/jquery-themes/base/*.css',
                'apps/tms/static/tms/js/jquery-themes/base/images/*',
                'apps/tms/static/tms/js/jquery-themes/ui-lightness/*.css',
                'apps/tms/static/tms/js/jquery-themes/ui-lightness/images/*',
                'apps/tms/static/tms/js/jquery-ui/*.js',
                'apps/tms/static/tms/js/jquery-ui/i18n/*.js',
                'apps/tms/static/tms/js/jquery-ui/minified/*.js',
                'static/uni_form/*',
                'templates/*.html',
                'templates/adlibre/contrib/widgets/*.html',
                'templates/admin/*.html',
                'templates/admin/tms/*.html',
                'templates/admin/tms/customer/*.html',
                'templates/admin/tms/job/*.html',
                'templates/admin/tms/project/*.html',
                'templates/admin/tms/services/*.html',
                'templates/pagination/*.html',
                'templates/registration/*.html',
                'templates/reporting/*.html',
                'templates/tms/*.html',
                'templates/tms/reports/*.html',
                'templates/uni_form/*.html',
            ], # this should be done automatically
        },
    data_files=[
        ('adlibre_tms', ['settings_prod.py', 'local_settings.py.example', 'manage.py']),
        ('db', ['db/.gitignore']), # create empty dir
        ('deployment', find_files('deployment', '*')),
        ('docs', find_files('docs', '*')),
        ('www', ['www/.gitignore']), # create empty dir
    ],
    install_requires=requirements,
)


