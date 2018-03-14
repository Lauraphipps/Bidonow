#!/bin/bash

set -e
set -x

docker stop webapp
docker container rm webapp
docker build -t webapp .
docker run -d --mount type=bind,src=/app/tmp/webapp/,dst=/tmp/ --name webapp webapp
service apache2 restart
