# Docker / CKAN upstream

OpenImperia uses the official CKAN Docker Compose project as its infrastructure
base.

- https://github.com/ckan/ckan-docker
- https://github.com/ckan/ckan-docker-base

The upstream Docker project is not vendored in v0.1, keeping this repository
small and making CKAN upgrades easier. A later release can vendor a pinned
snapshot while preserving upstream attribution and licensing.

## Hook di inizializzazione

L'immagine locale (`docker/ckan/Dockerfile`) aggiunge uno script in
`/docker-entrypoint.d/`. Il base image `ckan/ckan-base` esegue i file presenti
in quella cartella durante l'avvio, **dopo** l'inizializzazione del database e
la generazione della `SECRET_KEY`, ma prima di uwsgi. Lo script
`10-openimperia-init.sh` esegue `ckan ... openimperia init`, che crea in modo
idempotente l'organizzazione di default del portale.
