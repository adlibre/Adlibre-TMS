# FIXME: NB, this fabfile has not been updated for a while, and needs to be fixed before it can be used

import os

from fabric.api import *
from fabric.contrib.project import rsync_project
from fabric.contrib import files, console
from fabric import utils


RSYNC_EXCLUDE = (
    '.DS_Store',
    '.svn',
    '*.pyc',
    'etc',
    'logs',
    'whoosh_index',
    'pip-log.txt',
    'site_media',
    'local_settings.py',
    'fabfile.py',
    'bootstrap.py',
)
env.home = '/srv/www/tms'
env.website = 'tms.in.adlibre.net'
env.project = 'tms'


def _setup_path():
    env.root = os.path.join(env.home, env.environment)
    env.code_root = os.path.join(env.root, env.project)
    env.virtualenv_root = os.path.join(env.root, 'env')
    env.settings = 'settings_%(environment)s' % env

def staging():
    """ use staging environment on remote host"""
    env.user = 'root'
    env.environment = 'staging'
    env.hosts = ['76.74.156.184']
    _setup_path()


def production():
    """ use production environment on remote host"""
    utils.abort('Production deployment not yet implemented.')


def bootstrap():
    """ initialize remote host environment (virtualenv, deploy, update) """
    require('root', provided_by=('staging', 'production'))
    sudo('mkdir -p %(root)s' % env, user='wwwpub')
    sudo('mkdir -p %s' % os.path.join(env.home, 'log'), user='wwwpub')
    sudo('mkdir -p %s' % os.path.join(env.home, 'db'), user='wwwpub')
    create_virtualenv()
    deploy()
    update_requirements()


def create_virtualenv():
    """ setup virtualenv on remote host """
    require('virtualenv_root', provided_by=('staging', 'production'))
    args = '--clear --no-site-packages --python=/usr/bin/python2.6'
    sudo('virtualenv %s %s' % (args, env.virtualenv_root))


def deploy():
    """ rsync code to remote host """
    require('root', provided_by=('staging', 'production'))
    if env.environment == 'production':
        if not console.confirm('Are you sure you want to deploy production?',
                               default=False):
            utils.abort('Production deployment aborted.')
    # defaults rsync options:
    # -pthrvz
    # -p preserve permissions
    # -t preserve times
    # -h output numbers in a human-readable format
    # -r recurse into directories
    # -v increase verbosity
    # -z compress file data during the transfer
    extra_opts = '--omit-dir-times'
    rsync_project(
        env.root,
        exclude=RSYNC_EXCLUDE,
        delete=True,
        extra_opts=extra_opts,
    )
    # upload django.wsgi file
    source = os.path.join('deploy', 'django.wsgi')
    dest = os.path.join(env.code_root, 'deploy', '%(environment)s.wsgi' % env)
    files.upload_template(source, dest, env)
    # fix permissions
    sudo('chown -R wwwpub %s' % env.home)
    sudo('chmod -R a+rw %s' % env.home)


def update_requirements():
    """ update external dependencies on remote host """
    require('code_root', provided_by=('staging', 'production'))
    requirements = os.path.join(env.code_root, 'requirements')
    with cd(requirements):
        cmd = ['pip install']
        cmd += ['-E %(virtualenv_root)s' % env]
        cmd += ['--requirement %s' % os.path.join(requirements, 'apps.txt')]
        sudo(' '.join(cmd))


def update_apache_conf():
    """ update apache configuration to remote host """
    require('root', provided_by=('staging', 'production'))
    source = os.path.join('deploy', 'apache.conf')
    dest = os.path.join('/etc/httpd', 'conf.d', 'tms.conf')
    files.upload_template(source, dest, env, use_sudo=True)
    # reload apache
    apache_reload()


def apache_reload():
    """ reload Apache on remote host """
    require('root', provided_by=('staging', 'production'))
    sudo('/etc/init.d/httpd graceful')


def apache_restart():
    """ restart Apache on remote host """
    require('root', provided_by=('staging', 'production'))
    sudo('/etc/init.d/httpd restart')


def django_build_static():
    """ run build_static command on remote host """
    require('root', provided_by=('staging', 'production'))
    sudo('%s/bin/python %s/manage.py build_static --noinput' % (env.virtualenv_root, env.code_root), user='wwwpub')


# def reset_local_media():
#     """ Reset local media from remote host """
#     require('root', provided_by=('staging', 'production'))
#     media = os.path.join(env.code_root, 'site_media', 'media')
#     local('rsync -rvaz %s@%s:%s site_media/media' % (env.user, env.hosts[0], media))
