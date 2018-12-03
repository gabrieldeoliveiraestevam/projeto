#!/bin/bash

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:800
python manage.py createsuperuser
