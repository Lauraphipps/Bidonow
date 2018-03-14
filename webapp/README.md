# webapp


Build docker image

```
cd webapp
docker build -t webapp .

# test using webapp-admin
docker run -it -p 9090:9090 --link webapp-db:webapp-db --name webapp-admin webapp bash
python manage.py runserver 0.0.0.0:9090
wget 127.0.0.1:9090

# run webapp
docker run -d --mount type=bind,src=/app/volumes/webapp/,dst=/tmp/ --link webapp-db:webapp-db --name webapp webapp
```

## CREATE DB

```
CREATE ROLE bidonow WITH LOGIN PASSWORD 'xxxxxxxx';
CREATE DATABASE bidonow;
GRANT ALL PRIVILEGES ON DATABASE bidonow TO bidonow;
