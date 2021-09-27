# Provisioning a new site

[TOC]

## Required packages

* Nginx
* Python 3.9.7
* pyenv + pipenv
* Git

eg, on Ubuntu:

  ```bash=
  sudo apt-get update
  sudo apt-get upgrade
  sudo apt install nginx git
  sudo apt-get install -y --no-install-recommends make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
  ```

## Pyenv Install

  ```bash=
  git clone https://github.com/pyenv/pyenv.git ~/.pyenv

  echo -e 'if shopt -q login_shell; then' \
    '\n  export PYENV_ROOT="$HOME/.pyenv"' \
    '\n  export PATH="$PYENV_ROOT/bin:$PATH"' \
    '\n eval "$(pyenv init --path)"' \
    '\nfi' >> ~/.bashrc

  echo -e 'if [ -z "$BASH_VERSION" ]; then'\
    '\n  export PYENV_ROOT="$HOME/.pyenv"'\
    '\n  export PATH="$PYENV_ROOT/bin:$PATH"'\
    '\n  eval "$(pyenv init --path)"'\
    '\nfi' >>~/.profile

  echo 'if command -v pyenv >/dev/null; then eval "$(pyenv init -)"; fi' >> ~/.bashrc
  echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zprofile
  echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zprofile
  echo 'eval "$(pyenv init --path)"' >> ~/.zprofile

  echo 'eval "$(pyenv init -)"' >> ~/.zshrc

  source ~/.bashrc
  ```

  Install python version

  ```bash=
  pyenv install 3.9.7
  pyenv global 3.9.7
  ```

## Pipenv Setting

  ```bash=
  export PIPENV_VENV_IN_PROJECT=1
  ```

## Nginx Virtual Host config

* see nginx.template.conf
* replace DOMAIN with, e.g., kitty0825.me
* replace USER with, e.g., kitty

## Systemd service

* see gunicorn-systemd.template.service
* replace DOMAIN with, e.g., kitty0825.me
* replace USER with, e.g., kitty

## Folder structure

Assume we have a user account at /home/username

  ```bash=
  /home/username
  └── site
      ├── DOMAIN1
      │    ├── .venv
      │    ├── db.sqlite3
      │    ├── manage.py
      │    ├── static
      │    ├── Pipfile
      │    ├── Pipfile.lock
      │    └── repo
      │        └── .env
      └── DOMAIN2
          ├── db.sqlite3
          ├── etc
  ```
