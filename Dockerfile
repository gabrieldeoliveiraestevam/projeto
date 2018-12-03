FROM python:3.6.7
ENV PYTHONUNBUFFERED 1
    
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

