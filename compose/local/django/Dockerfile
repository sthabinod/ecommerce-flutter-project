ARG PYTHON_VERSION=3.10-slim-bullseye

FROM python:${PYTHON_VERSION} as python

COPY ./requirements .

RUN pip install -r local.txt

ARG APP_HOME=/app

WORKDIR ${APP_HOME}

COPY ./compose/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY . ${APP_HOME}
