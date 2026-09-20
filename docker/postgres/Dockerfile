# Immagine PostgreSQL per CKAN: oltre al DB di default crea all'avvio
# il DB di CKAN e quello del DataStore (ruolo read-only per la lettura).
#
# Script di init derivati dal progetto ckan-docker:
# https://github.com/ckan/ckan-docker/tree/master/postgresql

FROM postgres:16-alpine

COPY initdb/* /docker-entrypoint-initdb.d/