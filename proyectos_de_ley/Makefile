coverage:
	coverage run --source=. manage.py test -v 2 pdl --setting=proyectos_de_ley.settings.base
	coverage report -m
	coverage html

migrate:
	python ../migrate_db.py

migrate_small:
	python ../migrate_db_small.py

lint:
	flake8 pdl ../proyectos_de_ley
