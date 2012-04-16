#!/usr/bin/env python

from setuptools import setup

setup(name='adlibre_tms',
    version='0.1.0',
    long_description=open('README.md').read(),
    url='https://github.com/macropin/Adlibre-TMS',
    packages=['adlibre_tms'],
    scripts=['manage.py',],
    install_requires=[
        'BeautifulSoup==3.2.0',
        'Django==1.3.1',
        'django-any==0.2.0',
        'django-compressor==1.1.1',
        'django-pagination==1.0.7',
        'django-uni-form==0.7.0',
        'flup==1.0.3.dev-20110405'
        ],
    dependency_links = [
        ],
)