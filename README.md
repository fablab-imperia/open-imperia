# OpenImperia

Portale open data sperimentale per il territorio di Imperia, basato su CKAN.

## Struttura

- `ckan/` — estensione e personalizzazione grafica di CKAN
- `collectors/` — framework Python per acquisire e normalizzare dati
- `scripts/` — entrypoint per esecuzione manuale/cron
- `cron/` — esempio di configurazione cron
- `docs/` — documentazione tecnica

## Stato

Versione iniziale (`0.1`): struttura del progetto, estensione CKAN minima e framework dei collector.

La base Docker di CKAN è tenuta separata dal codice applicativo. Per il primo avvio si utilizza la configurazione Docker ufficiale di CKAN, aggiungendo questa estensione locale.

## Requisiti

- Linux
- Docker Engine
- Docker Compose v2
- Python 3.10+

## Avvio con Docker

Lo stack completo (`docker-compose.yml`) avvia: CKAN con l'estensione
`openimperia`, PostgreSQL (DB principale + DataStore), Solr, Redis,
Datapusher e un container `collectors` che esegue i collector via cron.

```bash
cp .env.example .env
#   - sostituire CKAN_API_KEY con una chiave API valida
#     (creata da un sysadmin nel portale: /user/<nome>, sezione API)
#   - cambiare CKAN_SYSADMIN_PASSWORD e CKAN___BEAKER__SESSION__SECRET
docker compose up --build -d
```

Il portale è disponibile su http://localhost:5000 (amministratore:
`CKAN_SYSADMIN_NAME` / `CKAN_SYSADMIN_PASSWORD`). I collector eseguono un
primo aggiornamento all'avvio e poi secondo `COLLECTOR_CRON_SCHEDULE`.

Comandi utili:

```bash
docker compose ps          # stato dei servizi
docker compose logs -f collectors   # log dei collector
docker compose exec ckan ckan -c /srv/app/ckan.ini search-index rebuild
docker compose down        # arresta (senza -v i dati restano su volumi)
```

## Collector

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r collectors/requirements.txt

PYTHONPATH=. python -m collectors --list
PYTHONPATH=. python -m collectors --source example --dry-run
```

Per pubblicare su CKAN:

```bash
export CKAN_URL=http://localhost:5000
export CKAN_API_KEY=...
PYTHONPATH=. python -m collectors --all
```

## Licenza

Il codice originale di OpenImperia è AGPL-3.0-or-later.

CKAN e le componenti upstream mantengono le proprie licenze.
