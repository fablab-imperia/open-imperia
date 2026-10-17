# Architettura

Open Data Imperia è composto da due parti che comunicano esclusivamente tramite
la CKAN Action API:

```text
                     OpenImperia
                          |
             +------------+------------+
             |                         |
            CKAN                   Collectors
       (portale + API)         (raccolta dati)
             |                         |
             |                  +------+------+
             |                  |             |
             |               Source A      Source B
             |                  |             |
             +------ CKAN API --+-------------+
```

## Componenti

### CKAN

Portale open data basato su CKAN 2.11, eseguito in Docker. Fornisce catalogo,
ricerca a faccette, organizzazioni, API e DataStore. È personalizzato per il
territorio di Imperia tramite l'estensione locale `ckanext-openimperia`.

Servizi dello stack (`docker-compose.yml`):

- **ckan** — applicazione web e API (immagine `openimperia/ckan:2.11`)
- **db** — PostgreSQL, con database dedicati a CKAN e al DataStore
- **solr** — ricerca e indicizzazione
- **redis** — cache e code interne
- **datapusher** — importazione automatica delle risorse tabellari
- **collectors** — container per l'esecuzione dei collector

### Estensione `ckanext-openimperia`

Il codice si trova in `ckan/src/ckanext-openimperia/` e implementa tre interfacce
CKAN (`ckanext/openimperia/plugin.py`):

- **IConfigurer** — registra le cartelle `templates/` e `public/`, applica il
  branding di default (titolo, descrizione, logo, testo introduttivo, lingua) e
  imposta la lista delle licenze (`licenses_group.json`). Il branding non
  sovrascrive valori impostati esplicitamente in `ckan.ini` o via variabili
  d'ambiente.
- **IActions** — concatena `package_create` per assegnare la licenza aperta di
  default (`cc-by`) ai nuovi dataset.
- **IClick** — fornisce il comando `ckan openimperia init`, invocato
  automaticamente all'avvio del container, che crea l'organizzazione
  `Fablab Imperia APS`.

Risorse incluse: template sovrascritti (`base.html`, `footer.html`,
`home/index.html`), foglio di stile e logo in `public/`, elenco licenze.

### Collectors

Framework Python in `collectors/` per raccogliere dati da fonti esterne e
pubblicarli su CKAN. Vedi `docs/adding-source.md` per creare una sorgente.

- **`core/ckan.py`** — `CKANClient`, wrapper dell'Action API con `upsert_dataset`
  idempotente (aggiorna se esiste, crea altrimenti).
- **`core/models.py`** — modello `Dataset` (titolo, note, tag, risorse).
- **`core/collector.py`** — classe base `DataSource` con `fetch()`,
  `transform()` e `run()`.
- **`core/registry.py`** — autodiscovery dei moduli in `sources/`.
- **`sources/`** — una classe `DataSource` per ogni sorgente dati.

Comandi:

```bash
PYTHONPATH=. python -m collectors --list
PYTHONPATH=. python -m collectors --source <nome> [--dry-run]
PYTHONPATH=. python -m collectors --all
```

## Principi

1. I collector non accedono direttamente al database CKAN.
2. La pubblicazione avviene tramite Action API.
3. Ogni sorgente è una classe `DataSource`.
4. L'autodiscovery permette di aggiungere una sorgente creando un modulo Python.
5. I segreti non vengono committati (variabili d'ambiente).
6. La configurazione del portale è dichiarativa: `ckan.ini` e variabili
   d'ambiente hanno la precedenza sui default dell'estensione.
