FROM python:3.6.7
ENV PYTHONUNBUFFERED 1
ENV DJANGO_DB_NAME=default
ENV DJANGO_SU_NAME=admin
ENV DJANGO_SU_EMAIL=admin@my.company
ENV DJANGO_SU_PASSWORD=mypass

WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV DJANGO_DB_NAME=default
ENV DJANGO_SU_NAME=admin
ENV DJANGO_SU_EMAIL=admin@my.company
ENV DJANGO_SU_PASSWORD=mypass

RUN python -c "import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'projeto.settings'
import django
django.setup()
from django.contrib.auth.management.commands.createsuperuser import get_user_model
if get_user_model().objects.filter(username='$DJANGO_SUPERUSER_USERNAME'): 
    print 'Super user already exists. SKIPPING...'
else:
    print 'Creating super user...'
    get_user_model()._default_manager.db_manager('$DJANGO_DB_NAME').create_superuser(username='$DJANGO_SUPERUSER_USERNAME', email='$DJANGO_SUPERUSER_EMAIL', password='$DJANGO_SUPERUSER_PASSWORD')
    print 'Super user created...'"