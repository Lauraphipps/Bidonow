FROM python:3.6-stretch

ENV INSTANCE_TYPE=prod

RUN pip install uwsgi

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["uwsgi", "--ini", "uwsgi.ini"]
