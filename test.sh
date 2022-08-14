#!/bin/sh
python manage.py collectstatic --noinput && \
pytest --ds=config.settings.test --cov=api --cov-report term-missing --capture=no --nomigrations --cov-config=.coveragerc $@ && \
flake8 