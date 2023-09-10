#!/bin/bash
fallocate -l 512M /swapfile
chmod 0600 /swapfile
mkswap /swapfile
echo 10 > /proc/sys/vm/swappiness
swapon /swapfile
echo 1 > /proc/sys/vm/overcommit_memory
gunicorn OnlineStoreDjango.wsgi:application --bind 0.0.0.0:8000
cp my_apps/shop/management/banners/* shop/media/foto/banners/
cp my_apps/shop/management/categories/* shop/media/foto/categories/
cp my_apps/shop/management/products/* shop/media/foto/products/
python manage.py set_database
