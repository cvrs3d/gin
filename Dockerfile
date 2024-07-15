FROM python:3.12-alpine
LABEL authors="ev.ustinov03@gmail.com"

COPY requirements.txt /temp/requirements.txt
COPY core /core
WORKDIR /core
EXPOSE 8080

RUN apk add postgresql-client build-base postgresql-dev
RUN python -m ensurepip --upgrade
RUN python -m pip install --upgrade setuptools
RUN pip install -r /temp/requirements.txt
RUN adduser --disabled-password service-user
USER service-user
