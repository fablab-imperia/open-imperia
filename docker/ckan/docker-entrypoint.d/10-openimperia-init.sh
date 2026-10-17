#!/bin/bash
# Hook di avvio del base image ckan/ckan-base: viene eseguito dopo l'init
# del database e la generazione della SECRET_KEY, prima di uwsgi.
# Crea in modo idempotente l'organizzazione di default del portale.
#
# NOTA: questo file viene "sourced" da start_ckan.sh: non usare "exit" e
# non far fallire l'avvio del container.

echo "[openimperia] Inizializzazione portale (organizzazione di default)..."
ckan -c "${CKAN_INI:-/srv/app/ckan.ini}" openimperia init \
    || echo "[openimperia] init fallito: verrà ritentato al prossimo avvio."
