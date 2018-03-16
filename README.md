# Bidonow application

## ENVIRONMENT VARIABLES

1. POSTGRES_PASSWORD - password to access postgres DB
2. INSTANCE_TYPE - type of instance. Possible values: *prod* and *dev*. If not defined we use *dev*. 

## Containers

### webapp (bidnow-webapp)

uwsgi server that run python/django code

### webapp-db (bidnow-db)

postgres db


### bidnow-bild

Build bidnow application

### HOST

Apache server 

## Volumes

### webclient (static)

Static resources required for webclient

Paths:

1. HOST: /volumes/bidnow-webclient
2. APACHE: /volumes/bidnow-webclient

Subfolders:
js
css
img
fonts


### bidnow-media

Files uploaded by users

Paths:

1. HOST: /volumes/bidnow-media/
2. APACHE: /volumes/bidnow-media/
3. bidnow-webapp: /var/bidnow-media/

Subfolders:

media - root folder for all files.

### bidnow-db

Postgres db

Paths:

1. HOST: /volumes/bidnow-db/
2. bidnow-db: /var/bidnow-db/

Subfolders:

logs - for logs
data - for DB data files

### uwsgi

Containes uwsgi socket for Apache proxy.

Paths:

1. HOST: /volumes/uwsgi/
2. bidnow-webapp: /var/uwsgi/
3. APACHE: /volumes/uwsgi

Subfolders:

logs - for logs
uwsgi.socket


## Applications



### webapp

Web site

### apache2

Apache2 config files and scripts

### webapp-db

Config files for Postgres DB for webapp

### volumes

Volumes folders for applications using in docker images

Structure:

volumes/
    webapp-db/ - volume for webaapp-db app
        data/ - DB files
    webapp/ - for webapp application
       media/ - for media data (images and files uploaded by user)
       static/ - static files
       uwsgi.sock - uwsgi socket file to communicate with web server (Apache2)




