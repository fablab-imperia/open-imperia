# Open Data Imperia — Presentazione Linux Day

## Slide 1 — Titolo
**Dai dati pubblici ai dati aperti: il progetto Open Data Imperia con CKAN**

Relatore: [Nome e cognome]  
Linux Day [edizione] — [luogo] — [data]

*Open Data Imperia • Fablab Imperia APS*

## Slide 2 — Chi sono e perché questo progetto
- **Chi parla:** [contesto: sviluppo software, PA, territorio]
- **Obiettivo:** "Vediamo cos'è l'open data, come la legge italiana lo impone, e come abbiamo iniziato a costruire un portale open data per Imperia con strumenti liberi."
- **Nota:** Progetto *sperimentale* e in evoluzione — invito a contribuire

## Slide 3 — Che cosa sono gli open data
> *"Dati che possono essere liberamente usati, riutilizzati e ridistribuiti da chiunque, al più con il vincolo di citarne la fonte e condividerli allo stesso modo"*  
> *(Open Definition — opendefinition.org)*

**I tre pilastri:**
- Disponibilità e accesso
- Riutilizzo e ridistribuzione  
- Partecipazione universale (nessuna discriminazione d'uso)

## Slide 4 — Cosa NON è un open data
- Un PDF scansionato (non facilmente riutilizzabile)
- Una pagina web senza download
- Un formato proprietario chiuso
- Una licenza con restrizioni non compatibili con la *Open Definition*

## Slide 5 — La "scala" delle 5 stelle di Tim Berners-Lee
1. ⭐ Dati disponibili online, qualunque formato
2. ⭐⭐ Dati strutturati (es. Excel)
3. ⭐⭐⭐ Formati non proprietari e aperti (CSV, JSON, XML)
4. ⭐⭐⭐⭐ URI permanenti per gli elementi
5. ⭐⭐⭐⭐⭐ Dati collegati (*Linked Data*) ad altri dataset

*AgID richiede almeno 3 stelle, raccomanda di puntare a 5*

## Slide 6 — Formati e interoperabilità
**Formati aperti:** CSV, JSON, XML, GeoJSON, RDF  
**Dati dinamici:** API REST

**Perché conta:** L'interoperabilità permette di *combinare* dataset diversi e costruire servizi nuovi

## Slide 7 — Esempi d'uso concreti
- **Trasporti:** orari e fermate per app di mobilità
- **Ambiente:** qualità dell'aria, aree verdi, spiagge
- **Trasparenza:** bilancio, contratti, spese
- **Turismo:** punti di interesse, eventi, strutture ricettive
- **Ricerca e giornalismo:** analisi civiche e *data journalism*

## Slide 8 — Chi ci guadagna
- **Cittadini:** trasparenza e controllo della cosa pubblica
- **Imprese e startup:** nuovi servizi, minor costo di accesso al dato
- **PA:** efficienza interna, meno richieste di accesso formale, immagine
- **Territorio:** narrazione dei dati locali, pianificazione

## Slide 9 — Un esempio locale
Quali dati pubblica già la Liguria / Imperia?  
L'obiettivo è renderli più facili da trovare e riutilizzare.

## Slide 10 — Il quadro europeo
- **2003/98/CE** — Prima direttiva PSI (riutilizzo informazione settore pubblico), modificata nel 2013
- **2013/37/UE** — Modifica alla direttiva PSI
- **Direttiva (UE) 2019/1024** — *Open Data Directive*, introduce *dati di elevato valore (HVD)* e *dati dinamici*
- **Regolamento di esecuzione (UE) 2023/138** — Individua le serie di dati di elevato valore

## Slide 11 — Il recepimento in Italia
- **D.Lgs. 24 gennaio 2006, n. 36** — Attuazione direttiva PSI
- **D.Lgs. 8 novembre 2021, n. 200** — Recepisce direttiva (UE) 2019/1024, modifica D.Lgs. 36/2006
  - Formati aperti, gratuità di principio
  - Tempi di risposta: 30 giorni lavorativi
  - Dati di elevato valore
- **In vigore dal 15 dicembre 2021**

## Slide 12 — Trasparenza e Codice dell'Amministrazione Digitale
- **D.Lgs. 14 marzo 2013, n. 33** — Riordino della disciplina sulla trasparenza (art. 9 → catalogo dati, metadati, banche dati)
- **D.Lgs. 7 marzo 2005, n. 82 (CAD)**
  - Art. 52 — Dati aperti e riutilizzo
  - Art. 68 — Sviluppo dei sistemi informativi
  - Art. 71 — Linee guida AgID

## Slide 13 — Le linee guida AgID
**Linee guida recanti regole tecniche per l'apertura dei dati e il riutilizzo dell'informazione del settore pubblico** *(AgID, determina n. 183/2023)*

**Requisiti chiave:**
- ≥ **3 stelle**
- Formati aperti
- Licenze esplicite
- API per i dati dinamici
- Metadati conformi al profilo **DCAT-AP_IT**

## Slide 14 — Metadati e catalogazione: DCAT-AP_IT
- **DCAT** (*Data Catalog Vocabulary*) → **DCAT-AP** (profilo europeo) → **DCAT-AP_IT** (profilo italiano)
- Ogni dataset: titolo, descrizione, temi, titolare, frequenza aggiornamento, distribuzioni, licenza
- **Harvesting** permette la federazione: comuni → regioni → **dati.gov.it** → portale europeo

## Slide 15 — dati.gov.it e la federazione
- **dati.gov.it** — portale nazionale dei dati aperti *(riferimento unico ex art. 1 comma 8, D.Lgs. 102/2015)*
- Le Regioni svolgono spesso il ruolo di **aggregatori territoriali**
- **Liguria:** `dati.regione.liguria.it` (catalogo regionale basato su CKAN)

## Slide 16 — Licenze
- **IODL 2.0** *(Italian Open Data License, AgID)*
- **CC BY 4.0**, **CC BY-SA 4.0**, **CC0 1.0**

**Messaggio:** La licenza deve essere *esplicita* e compatibile con la *Open Definition*.  
**Nel nostro portale:** licenza di default **CC BY 4.0**

## Slide 17 — Obiettivi del progetto
- **Iniziativa di Fablab Imperia APS:** portale open data civico per il territorio, libero e replicabile
- Rendere i dati locali **trovabili, riusabili e catalogati**
- Automatizzare la raccolta dei dati da fonti online con codice Python schedulato

## Slide 18 — Perché CKAN
- Piattaforma *open source* (AGPL) per cataloghi di dati
- Usata da PA e governi in tutto il mondo
- Funzionalità: catalogo, ricerca a faccette, organizzazioni, API, DataStore, *harvesting*, estensioni
- **Base solida** invece di reinventare la ruota

## Slide 19 — Architettura tecnica
**Schema:** `CKAN` ⟷ `Collectors` ⟷ sorgenti esterne (via API)

**Componenti Docker:**
- CKAN, PostgreSQL (+ DataStore), Solr, Redis, Datapusher
- Container *collectors*
- Immagine CKAN + estensione locale `ckanext-openimperia`

*(Vedi diagramma in `docs/architecture.md`)*

## Slide 20 — Il portale oggi (personalizzazione)
- Branding **Open Data Imperia** (logo, tema, home)
- Lingua italiana, organizzazione **Fablab Imperia APS**
- Licenze italiane + default **CC BY 4.0**
- Sito volutamente **vuoto**: lo popoleremo con i *collector*
- Demo: `http://localhost:5000`

## Slide 21 — I collector: l'idea
- **Classi Python** che estraggono dati da fonti online, li normalizzano e li pubblicano su CKAN via *Action API*
- **Nessun accesso diretto** al database: usa l'API → architettura pulita e stabile
- **Esecuzione schedulata** (cron) per mantenere i dati aggiornati

## Slide 22 — Anatomia di una sorgente
**Classe che eredita da `DataSource`:**
- `fetch()` → scarica i dati grezzi
- `transform(raw)` → restituisce un `Dataset` (titolo, note, tag, risorse)
- `validate()` / `run(dry_run)` → pubblica o simula

**Autodiscovery:** basta aggiungere un file in `collectors/sources/`  
**Comandi:** `python -m collectors --list`, `--source`, `--all`, `--dry-run`

## Slide 23 — Il client CKAN
- `CKANClient.upsert_dataset()` usa `package_show` + `package_create/update`
- **Idempotente:** rieseguire un *collector* aggiorna, non duplica
- Configurazione via variabili d'ambiente (URL + API key), **segreti non nel repo**

## Slide 24 — Struttura del codice
- **`collectors/core/`** — framework (*DataSource*, *CKANClient*, orchestrazione)
- **`collectors/sources/`** — sorgenti specifiche
- Separazione chiara tra logica generica e logica per ogni fonte

## Slide 25 — Roadmap: le fonti dati per Imperia
- **Regione Liguria** — *harvesting* catalogo CKAN `dati.regione.liguria.it`
- **ISTAT** — popolazione e statistiche comunali via API SDMX
- **MIMIT** — prezzi carburanti (CSV ufficiale), filtrati per provincia di Imperia
- **OpenStreetMap / Overpass** — punti di interesse del comune
- **Metadati DCAT-AP_IT** e *harvesting* verso `dati.gov.it`

## Slide 26 — Licenza e riuso del progetto
- **Codice:** *AGPL-3.0-or-later* — libero, modificabile, con obbligo di condivisione delle modifiche se esposto come servizio
- **Dati:** con licenza aperta (default *CC BY 4.0*)
- **Invito:** altri comuni e gruppi possono partire da questa base per replicare il progetto

## Slide 27 — Demo live
**Sequenza:**
```bash
# 1) Avvio dello stack
docker compose up --build -d
docker compose ps

# 2) Aprire il portale
# http://localhost:5000

# 3) Verificare organizzazione
curl -s http://localhost:5000/api/3/action/organization_list

# 4) Elenco collector
PYTHONPATH=. python -m collectors --list

# 5) Test in dry-run
PYTHONPATH=. python -m collectors --source example --dry-run
```

*Piano B:* screenshot/video in caso di problemi con Docker/rete

## Slide 28 — Cosa abbiamo visto
- **Open data:** definizione, 5 stelle, valore per cittadini/PA/imprese
- **Normativa:** direttiva UE 2019/1024, D.Lgs. 36/2006 e 200/2021, D.Lgs. 33/2013, CAD, linee guida AgID, DCAT-AP_IT, dati.gov.it
- **Caso concreto:** CKAN + collector Python per Imperia, con strumenti liberi e licenza aperta

## Slide 29 — Come contribuire / riutilizzare
- **Codice:** [repository GitHub del progetto]
- **Prossimi passi:** implementare i collector, esporre DCAT-AP_IT, test con dati reali
- **Contributi benvenuti:** segnalazioni, nuove fonti dati, miglioramenti
- **Contatti:** Fablab Imperia APS

## Slide 30 — Grazie / Domande
**Grazie per l'attenzione!**

- **Repository:** [QR code]
- **Portale:** [QR code]
- **Contatti:** [info contatti]

*Domande?*
