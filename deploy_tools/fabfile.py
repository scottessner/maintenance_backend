from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

# For use:
# Navigate to the deploy_tools folder
# Run: fab deploy:sitename=api.maintenance.ssessner.com
# When prompted for host use: bernadette

REPO_URL = 'https://github.com/scottessner/maintenance_backend.git'

def deploy(sitename):
    site_folder = '/home/{0}/sites/{1}'.format(env.user, sitename)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, sitename)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)

def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p {0}/{1}'.format(site_folder, subfolder))

def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd {0} && git fetch'.format(source_folder))
    else:
        run('git clone {0} {1}'.format(REPO_URL, source_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd {0} && git reset --hard {1}'.format(source_folder, current_commit))

def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/maintenance_backend/settings.py'
    sed(settings_path, 'DEBUG = True', 'DEBUG = False')
    sed(settings_path, 
        'ALLOWED_HOSTS = .+$',
        'ALLOWED_HOSTS = ["{0}"]'.format(site_name))
    sed(settings_path,
        'database/db.sqlite3',
        '../database/db.sqlite3')
    secret_key_file = source_folder + '/maintenance_backend/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcedfghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '{0}'".format(key))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3 {0}'.format(virtualenv_folder))
    run('{0}/bin/pip install -r {1}/requirements.txt'.format(
        virtualenv_folder, source_folder))

def _update_static_files(source_folder):
    run('cd {0} && ../virtualenv/bin/python3 manage.py collectstatic --noinput'.format(source_folder))

def _update_database(source_folder):
    run('cd {0} && ../virtualenv/bin/python3 manage.py migrate --noinput'.format(source_folder))
