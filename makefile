hooks_setup:
	pip install black flake8 isort[pyproject] pre-commit
	pre-commit install

run:
	docker-compose up --build

stop:
	docker-compose stop

shell:
	docker-compose run --rm app python manage.py shell

superuser:
	docker-compose run --rm app python manage.py createsuperuser

# usage - `make app name=NAME`
app:
	docker-compose run --rm app python manage.py startapp $(name)

# usage - `make migrations app=APP`
migrations:
	docker-compose run --rm app python manage.py makemigrations $(app)

migrate:
	docker-compose run --rm app python manage.py migrate

# you can pass pytest args, e.g. `make test args='-k test_landing_page'` to run a single test
test:
	docker-compose run --rm app ./test.sh $(args)

reqs:
	pip-compile requirements/base.in
	pip-compile requirements/test.in
	pip-compile requirements/local.in
	docker-compose build

reqs_upgrade:
	pip-compile --upgrade requirements/base.in
	pip-compile --upgrade requirements/test.in
	pip-compile --upgrade requirements/local.in
	docker-compose build

# usage - `make load_fixtures file=FILE`
load_fixtures:
	docker-compose run --rm app python manage.py loaddata $(file)

# usage - `make dump_fixtures file=FILE`
dump_fixtures:
	docker-compose run --rm app python manage.py dumpdata --all --indent=2 > $(file)

    