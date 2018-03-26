# Backup bidonow DB


# Build
```
docker build -t webapp-db-backup -f Dockerfile .
```

# Run

```
docker run -it --name webapp-db-backup --mount type=bind,src=/app/volumes/webapp-db-backups/,dst=/var/lib/webapp-db-backups/ --link webapp-db:webapp-db webapp-db-backup  bash
# inside docker container
pg_dump -h webapp-db -U bidonow > /var/lib/webapp-db-backups/bidonow_20180327.sql
exit
docker container rm webapp-db-backup
```
