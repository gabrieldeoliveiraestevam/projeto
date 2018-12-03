#!/bin/bash

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver 172.29.68.210:8000
python manage.py createsuperuser
