# Bidonow application

## ENVIRONMENT VARIABLES

1. POSTGRES_PASSWORD - password to access postgres DB
2. INSTANCE_TYPE - type of instance. Possible values: *prod* and *dev*. If not defined we use *dev*. 


## webapp

Web site

## apache2

Apache2 config files and scripts

## webapp-db

Config files for Postgres DB for webapp

## volumes

Volumes folders for applications using in docker images

Structure:

volumes/
    webapp-db/ - volume for webaapp-db app
        data/ - DB files
    webapp/ - for webapp application
       media/ - for media data (images and files uploaded by user)
       static/ - static files
       uwsgi.sock - uwsgi socket file to communicate with web server (Apache2)




