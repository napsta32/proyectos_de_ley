serve:
	cd proyectos_de_ley; python ./manage.py runserver --settings=proyectos_de_ley.settings.local

migrations:
	cd proyectos_de_ley; python ./manage.py makemigrations --settings=proyectos_de_ley.settings.local
	cd proyectos_de_ley; python ./manage.py migrate --settings=proyectos_de_ley.settings.local

stats:
	cd proyectos_de_ley; python ./manage.py create_stats --settings=proyectos_de_ley.settings.local
