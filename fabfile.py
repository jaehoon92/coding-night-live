from fabric.contrib.files import append, exists, sed, put
from fabric.api import env, local, sudo, run

import os
import json
import random

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)

with open(os.path.join(PROJECT_DIR, 'deploy.json')) as f:
    envs = json.loads(f.read())

REPO_URL = envs['REPO_URL']
PROJECT_NAME = envs['PROJECT_NAME']
REMOTE_HOST_SSH = envs['REMOTE_HOST_SSH']
REMOTE_HOST = envs['REMOTE_HOST']
REMOTE_USER = envs['REMOTE_USER']
REMOTE_PASSWORD = envs['REMOTE_PASSWORD']

STATIC_ROOT_NAME = 'collected_static'
STATIC_URL_NAME = 'static'

env.user = REMOTE_USER
username = env.user
env.hosts = [
    REMOTE_HOST_SSH,
]

env.password = REMOTE_PASSWORD

project_folder = '/home/{}/{}'.format(env.user, PROJECT_NAME)

apt_requirements = [
    'git',
    'python3-dev',
    'python3-pip',
    'build-essential',
    'libpq-dev',
    'python3-setuptools',
    'nginx',
    'postgresql',
    'postgresql-contrib',
    'redis-server',
]

def new_server():
    setup()
    deploy()

def setup():
    _get_latest_apt()
    _install_apt_requirements(apt_requirements)
    _make_virtualenv()

def deploy():
    _get_latest_source()
    _update_static_files()
    _update_database()
    _make_virtualhost()
    _grant_nginx()
    _grant_postgresql()
    _restart_nginx()

def _get_latest_apt():
    sudo('sudo apt-get install update && sudo apt-get -y upgrade')

def _install_apt_requirements(apt_requirements):
    reqs = ''
    for req in apt_requirements:
        reqs += (' ' + req)
    sudo('sudo apt-get -y install {}'.format(reqs))

def _get_latest_source():
    run('git clone %s %s' % (REPO_URL, project_folder))

def _update_settings():
    settings_path = project_folder + '/{}/settings.py'.format(PROJECT_NAME)
    sed(settings_path, 'DEBUG = TRUE', 'DEBUG = FALSE')
    sed(settings_path,
        'ALLOWED_HOSTS = .+$',
        'ALLOWED_HOSTS = ["%s"]' % (REMOTE_HOST,)
    )

def _update_static_files():
    run('cd %s && python3 manage.py collectstatic --noinput' % (project_folder))

def _update_database():
    sudo('cd %s && python3 manage.py migrate --noinput' % (project_folder))

# nginx conf file..
def _make_virtualhost():
    script = """'
    '""".format(
        static_root=STATIC_ROOT_NAME,
        username=env.user,
        project_name=PROJECT_NAME,
        static_url=STATIC_URL_NAME,
        servername=REMOTE_HOST
    )

def _grant_nginx():
    pass

def _grant_postgresql():
    pass

def _restart_nginx():
    sudo('sudo systemctl restart nginx')
