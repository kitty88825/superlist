from random import SystemRandom

from string import ascii_letters, digits

from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run


REPO_URL = 'https://github.com/kitty88825/superlist.git'


def deploy():
    site_folder = f'/home/{env.user}/site/{env.host}'
    run(f'mkdir -p {site_folder}')
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()


def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} .')

    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'git reset --hard {current_commit}')


def _update_virtualenv():
    if not exists('.venv'):
        run(f'pip install pipenv')
        run(f'pipenv install --python 3.9.7')

    run('pipenv install')


def _create_or_update_dotenv():
    allowed_hosts_text = f's/ALLOWED_HOSTS=.*/ALLOWED_HOSTS={env.host}/'
    extension = allowed_hosts_text

    if not exists('superlists/.env'):
        run(f'cp superlists/example.env superlists/.env')
        new_secret_key = ''.join(SystemRandom().choices(f'{ascii_letters}{digits}', k=50))
        secret_text = f's/SECRET_KEY=/SECRET_KEY={new_secret_key}/'
        extension = f'{secret_text}; {allowed_hosts_text}'

    run(f"sed -i '{extension}' superlists/.env")
