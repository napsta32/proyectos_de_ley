- pip install virtualenv
- pip install virtualenvwrapper
- edit .bashrc or .bash_profile files:
    - export WORKON_HOME=$HOME/.virtualenvs
    - source /usr/local/bin/virtualenvwrapper.sh
- mkvitualenv -p /usr/bin/python3 myenvironment
- pip install -r requirements.txt
- if using python3.2 reinstall Markupsafe with [this pull request](https://github.com/mitsuhiko/markupsafe/pull/32).
- create settings file: production.py
- create config.json file with keys and crawlera user and pass
- install mod_wsgi python 3
- activate that module by adding Loadmodule wsgi_module mod_wsgi.so to Apache's conf file.
- configure virtual host in Apache with WSGI python path and deamon. Python path should also point to the virtualenvironment.
- configure the database:
    python manage.py makemigrations --settings=proyectos_de_ley.settings.production
    python manage.py migrate --settings=proyectos_de_ley.settings.production
    make migrate
    sudo chown www-data:www-data -R *
- set the scraper as a cronjob:
    - sudo su -c "crontab -e" www-data
