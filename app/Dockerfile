# FROM python:alpine
FROM python

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app /static /media
WORKDIR /app

#RUN apk update 
#RUN apk add --no-cache --virtual .build-deps \
#                                linux-headers \
#                                libffi-dev \
#                                zlib-dev \
#                                gcc g++\
#                                musl-dev \
#                                postgresql-dev postgresql-client \
#                                python3-dev \
#                                py3-numpy py3-pandas

RUN apt-get update && apt-get install -y python3-dev python3-pip musl-dev build-essential libpq-dev

RUN pip install --upgrade pip
RUN pip install setuptools wheel
COPY ./requirements.txt .
RUN pip install --no-cache-dir --default-timeout=500 -r requirements.txt

#RUN apk del gcc python3-dev libffi-dev musl-dev

CMD while ! python3 manage.py sqlflush > /dev/null 2>&1 ; do sleep 1 ; done && \
    echo 'line 31' && \
    python3 manage.py makemigrations --noinput && \
    echo 'line 33' && \
    python3 manage.py migrate --noinput && \
    echo 'line 35' && \
    python3 manage.py collectstatic --noinput && \
    echo 'line 37' && \
    python3 manage.py createsuperuser_if_none_exists --user=amir --password=amir1374 --email=amirayat20@gmail.com; \
    gunicorn -w 5 -b 0.0.0.0:8000 core.asgi:application -k uvicorn.workers.UvicornWorker