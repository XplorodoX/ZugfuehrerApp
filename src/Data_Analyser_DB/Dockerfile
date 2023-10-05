FROM postgres:latest

ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD example

COPY init.sql /docker-entrypoint-initdb.d/

CMD ["postgres"]