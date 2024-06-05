FROM postgres:latest

ENV POSTGRES_DB=statistics_app
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

EXPOSE 5432

COPY init.sql /docker-entrypoint-initdb.d/