FROM python:3.11-slim

RUN mkdir /server && apt-get update && apt-get install -y git
WORKDIR /server

COPY ./poetry.lock /server/
COPY ./pyproject.toml /server/

RUN pip install poetry && poetry config virtualenvs.create false && poetry install

COPY ./ /server/
