- create settings file: production.py
- create config.json file with keys and crawlera user and pass
- install mod_wsgi python 3
- activate that module by adding Loadmodule mod_wsgi.so to Apache's conf file.
- configure virtual host in Apache with WSGI python path and dameon. Python
path should also point to the virtualenvironment.
- configure the database:
    python manage.py makemigrations --settings=proyectos_de_ley.settings.production
    python manage.py migrate --settings=proyectos_de_ley.settings.production
    make migrate
    sudo chown www-data:www-data -R *
