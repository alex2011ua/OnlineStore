#!/bin/bash
fallocate -l 512M /swapfile
chmod 0600 /swapfile
mkswap /swapfile
echo 10 > /proc/sys/vm/swappiness
swapon /swapfile
echo 1 > /proc/sys/vm/overcommit_memory
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py set_database
gunicorn OnlineStoreDjango.wsgi:application --bind 0.0.0.0:8000

