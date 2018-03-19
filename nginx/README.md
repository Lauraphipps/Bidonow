# NGINX web server to run webapp and serv static content


### Run nginx container

```
docker run --name webapp-nginx -p 80:80 -v /app/nginx/nginx.conf:/etc/nginx/nginx.conf:ro -v /app/volumes/webapp:/webapp:ro -d nginx
```


