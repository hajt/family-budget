FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt update && apt install -y libpq-dev gcc

COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/local.txt \
    && rm -rf /requirements

COPY ./docker/local/django/start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh
RUN chmod +x /start.sh

WORKDIR /app
