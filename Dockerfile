FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code/bolbol

# Sistem tələbləri
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Python tələbləri
COPY requirements.txt /code/
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r /code/requirements.txt

# Layihəni kopyala
COPY . /code/

# Statik faylları topla
# RUN python manage.py collectstatic --noinput
