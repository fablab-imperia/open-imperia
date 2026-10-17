# Immagine CKAN con l'estensione OpenImperia installata.
#
# La base ufficiale ckan/ckan-base:2.11 gestisce configurazione, migrazioni
# del DB e creazione del sysadmin partendo dalle variabili d'ambiente
# (vedi .env / docker-compose.yml). Qui aggiungiamo solo l'estensione locale.

FROM ckan/ckan-base:2.11

# Installa l'estensione OpenImperia in modalità editable: eventuali volumi
# montati sulla stessa path vengono rilevati in fase di avvio del container.
# La source resta di proprietà di ckan; l'installazione serve root perché
# l'utente ckan non ha diritti di scrittura su site-packages.
COPY --chown=ckan:ckan-sys ckan/src/ckanext-openimperia /srv/app/src_extensions/ckanext-openimperia

USER root
RUN pip install -e /srv/app/src_extensions/ckanext-openimperia
# Hook di avvio: crea l'organizzazione di default dopo l'init del DB
COPY docker/ckan/docker-entrypoint.d/10-openimperia-init.sh /docker-entrypoint.d/10-openimperia-init.sh
RUN chmod +x /docker-entrypoint.d/10-openimperia-init.sh
USER ckan