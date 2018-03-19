FROM python:3.6-stretch

RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt-get update && apt-get install -y nodejs yarn


ENV INSTANCE_TYPE=prod

RUN pip install uwsgi

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["uwsgi", "--ini", "uwsgi.ini"]
