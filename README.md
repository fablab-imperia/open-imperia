# OpenImperia

Portale open data sperimentale per il territorio di Imperia, basato su CKAN.

## Struttura

- `ckan/` — estensione e personalizzazione grafica di CKAN
- `collectors/` — framework Python per acquisire e normalizzare dati
- `scripts/` — entrypoint per esecuzione manuale/cron, smoke test, generazione `.env`
- `cron/` — esempio di configurazione cron
- `docker/` — Dockerfile di CKAN, collector, PostgreSQL e Caddy (`Caddyfile`)
- `docs/` — documentazione tecnica
- `docker-compose.yml` — stack di **sviluppo** (sito su `http://localhost:5000`)
- `docker-compose.prod.yml` — stack di **produzione** (Caddy + HTTPS)

## Stato

Versione iniziale (`0.1`): struttura del progetto, estensione CKAN con
personalizzazione per il territorio di Imperia e framework dei collector.

Roadmap a step:

1. **Portale personalizzato** (fatto): CKAN con branding "Open Data Imperia",
   organizzazione `Fablab Imperia APS`, licenze italiane e licenza di default
   CC BY 4.0. Il sito è volutamente **vuoto** (nessun dataset).
2. **Presentazione Linux Day**: scaletta del talk in
   [`docs/linux-day-presentazione.md`](docs/linux-day-presentazione.md).
3. **Online** (in corso): stack di produzione con Caddy e HTTPS su VPS
   ([`docs/deploy.md`](docs/deploy.md)).
4. **Popolamento**: implementazione dei collector (Regione Liguria, ISTAT,
   MIMIT carburanti, OSM, ...) e metadati DCAT-AP_IT.

La base Docker di CKAN è tenuta separata dal codice applicativo. Per il primo avvio si utilizza la configurazione Docker ufficiale di CKAN, aggiungendo questa estensione locale.

## Personalizzazione per Imperia

L'estensione `ckanext-openimperia` (`ckan/src/ckanext-openimperia`) fornisce:

- **Branding**: titolo, descrizione, logo (`public/images/openimperia-logo.svg`)
  e foglio di stile (`public/css/openimperia.css`) del portale.
- **Home page** personalizzata con hero e schede informative.
- **Lingua predefinita** italiano.
- **Organizzazione di default** `Fablab Imperia APS` (`fablab-imperia-aps`),
  creata automaticamente al primo avvio.
- **Licenze** italiane (CC BY 4.0, CC BY-SA 4.0, CC0 1.0, IODL 2.0, ODC-By,
  ODbL) definite in `licenses_group.json`, con **licenza di default CC BY 4.0**
  applicata a ogni nuovo dataset.

Le variabili di branding sono in `.env` (`CKAN__SITE_TITLE`, ecc.); i valori
nel file hanno sempre la precedenza sui default dell'estensione.

Comando di inizializzazione (eseguito automaticamente dall'immagine Docker,
riutilizzabile a mano):

```bash
docker compose exec ckan ckan -c /srv/app/ckan.ini openimperia init
```

## Requisiti

- Linux
- Docker Engine
- Docker Compose v2
- Python 3.10+

## Avvio in sviluppo

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

## Test

Smoke test del portale (home, API, organizzazione, licenze, asset statici;
con `CKAN_API_KEY` verifica anche la licenza di default in scrittura):

```bash
BASE_URL=http://localhost:5000 ./scripts/smoke-test.sh
```

## Deploy in produzione

Stack separato con **Caddy**, HTTPS automatico (Let's Encrypt), segreti reali,
porte di CKAN non esposte e limiti di memoria. Vedi la guida completa:
[`docs/deploy.md`](docs/deploy.md).

```bash
./scripts/gen-prod-env.sh            # genera .env con segreti casuali
docker compose -f docker-compose.prod.yml up -d --build
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
