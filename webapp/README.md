# webapp


Build docker image

```
cd webapp
docker build -t webapp .

# test using webapp-admin
docker run -it -p 9090:9090 --link webapp-db:webapp-db --mount type=bind,src=/app/volumes/webapp/,dst=/var/webapp --name webapp-admin webapp bash
python manage.py runserver 0.0.0.0:9090
wget 127.0.0.1:9090

# run webapp
docker run -d --mount type=bind,src=/app/volumes/webapp/,dst=/var/webapp --link webapp-db:webapp-db --name webapp webapp
```

## Deploy process

```
docker stop webapp
docker container rm webapp
docker rmi webapp:prev
docker tag webapp:latest webapp:prev
docker build -t webapp:latest .
docker run -it --link webapp-db:webapp-db --mount type=bind,src=/app/volumes/webapp/,dst=/var/webapp --name webapp-admin webapp:latest bash
    # inside docker
    python manage.py migrate
    # TODO check if we can use webpack to copy static files
    python manage.py collectstatic --clear --no-input
    exit
docker container rm webapp-admin
docker run -d --mount type=bind,src=/app/volumes/webapp/,dst=/var/webapp --link webapp-db:webapp-db --name webapp webapp:latest
sudo service apache2 restart
```

## Static files

TODO Read: https://medium.com/a-beginners-guide-for-webpack-2
TODO Example of webpack.config.js: https://github.com/Dogfalo/materialize/issues/4521

### Intall tools

1. yarn
2. sass - version 3.5.5 # TODO find way how to use webpack to build sass files

#### Install packages

```
yarn install
```

#### Build

```
npm run build
```


#### Compile sass

TODO Find way how to use webpack to build sass

```
sass .\static\sass\main.scss .\static\dist\main.css
```

## CREATE DB

```
CREATE ROLE bidonow WITH LOGIN PASSWORD 'xxxxxxxx';
CREATE DATABASE bidonow;
GRANT ALL PRIVILEGES ON DATABASE bidonow TO bidonow;
