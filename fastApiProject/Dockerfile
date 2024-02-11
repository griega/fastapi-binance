FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir /app

ENV POETRY_HOME /opt/poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-root

COPY . /app/

ENV PYTHONPATH .

EXPOSE 9999

CMD ["bash", "./start.sh"]
