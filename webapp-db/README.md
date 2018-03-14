# Postgres DB for web application

```
docker build -t webapp-db .
docker run -d -e POSTGRES_PASSWORD --mount type=bind,src=/app/volumes/webapp-db/data/,dst=/var/lib/postgresql/data/pgdata/ --name webapp-db webapp-db
```

# TEST DB connection
docker build -t webapp-db-client -f Dockerfile.db_client .
docker run -it -e POSTGRES_PASSWORD --name webapp-db-client --link webapp-db:webapp-db webapp-db-client bash
psql -h webapp-db -U bidonow
```
