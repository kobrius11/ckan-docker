FROM postgis/postgis:17-3.5-alpine

# Include datastore setup scripts
COPY --chown=postgres:postgres docker-entrypoint-initdb.d /docker-entrypoint-initdb.d
