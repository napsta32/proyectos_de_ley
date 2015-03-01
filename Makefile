serve:
	cd proyectos_de_ley; python ./manage.py runserver --settings=proyectos_de_ley.settings.local

migrations:
	cd proyectos_de_ley; python ./manage.py makemigrations --settings=proyectos_de_ley.settings.local
	cd proyectos_de_ley; python ./manage.py migrate --settings=proyectos_de_ley.settings.local

stats:
	cd proyectos_de_ley; python ./manage.py create_stats --settings=proyectos_de_ley.settings.local

coverage:
	coverage run --source proyectos_de_ley proyectos_de_ley/manage.py test -v 2 pdl search_advanced \
	    seguimientos stats --settings=proyectos_de_ley.settings.testing
	coverage report -m
	coverage html

rebuild_index:
	python proyectos_de_ley/manage.py rebuild_index --noinput --settings=proyectos_de_ley.settings.local
