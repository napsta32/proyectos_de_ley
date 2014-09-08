coverage:
	coverage run --source=. manage.py test pdl --setting=proyectos_de_ley.settings.local
	coverage report -m
	coverage html

migrate:
	python ../migrate_db.py
