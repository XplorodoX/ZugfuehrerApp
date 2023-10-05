# Autor: Florian Merlau
FROM timescale/timescaledb:latest-pg13

ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD example

COPY init.sql /docker-entrypoint-initdb.d/

CMD ["postgres", "-c", "shared_preload_libraries=timescaledb"]
