#!/usr/bin/env python

import os
import glob

from setuptools import setup


def is_package(path):
    return (
        os.path.isdir(path) and
        os.path.isfile(os.path.join(path, '__init__.py'))
        )

def find_packages(path, base="" ):
    """ Find all packages in path """
    packages = {}
    for item in os.listdir(path):
        dir = os.path.join(path, item)
        if is_package( dir ):
            if base:
                module_name = "%(base)s.%(item)s" % vars()
            else:
                module_name = item
            packages[module_name] = dir
            packages.update(find_packages(dir, module_name))
    return packages


setup(name='adlibre_tms',
    version='0.1.0',
    long_description=open('README.md').read(),
    url='https://github.com/macropin/Adlibre-TMS',
    packages=find_packages('.'),
    scripts=[],
    package_data={ 'adlibre_tms': ['templates/*',] },
    data_files = [
            ('adlibre_tms', ['local_settings.py', 'adlibre_tms/manage.py']),
            ('db', ['db/.gitignore']),
            ('deployment', glob.glob('deployment/*')),
            ('docs', glob.glob('docs/*')),
            ('www', glob.glob('www/*')),
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
    dependency_links = [
        ],
)
