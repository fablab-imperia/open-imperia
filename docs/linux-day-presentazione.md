# Open Data Imperia — scaletta presentazione Linux Day

**Titolo proposto:** _Dai dati pubblici ai dati aperti: il progetto Open Data Imperia con CKAN_

**Durata:** ~40 minuti (28–32 min di contenuti + demo + 8–10 min di domande)
**Pubblico:** pubblico tecnico e non del Linux Day (studenti, appassionati, cittadinanza digitale, PA locali)
**Prerequisiti:** nessuno tecnico. La demo userebbe il portale già avviato.

**Obiettivo del talk:** spiegare cosa sono gli open data, cosa prevede la normativa
italiana, e mostrare un caso concreto — il portale Open Data Imperia costruito su
CKAN con collector Python in licenza libera — come esempio riproducibile da altri
comuni e gruppi di volontari.

---

## Scaletta con tempi

| # | Sezione | Tempo | Slide |
|---|---------|-------|-------|
| 0 | Apertura e presentazione | 2' | 1–2 |
| 1 | Che cosa sono gli open data | 8' | 3–9 |
| 2 | La normativa italiana ed europea | 9' | 10–16 |
| 3 | Il progetto Open Data Imperia | 14' | 17–26 |
| 4 | Demo live | 4' | 27 |
| 5 | Conclusioni, riuso e domande | 3' + Q&A | 28–30 |

Consiglio: preparare **30 slide** al massimo, con poche parole ciascuna. Il valore
sta nel racconto, non nella densità delle slide.

---

## Sezione 0 — Apertura (2', slide 1–2)

**Slide 1 — Titolo**
- Titolo, sottotitolo, nome relatore, Linux Day (edizione, luogo, data).
- Logo Open Data Imperia e logo Linux Day.

**Slide 2 — Chi sono e perché questo progetto**
- Chi parla (contesto: sviluppo software, PA, territorio).
- Una frase di obiettivo: «Vediamo cos'è l'open data, come la legge italiana lo
  impone, e come abbiamo iniziato a costruire un portale open data per Imperia
  con strumenti liberi.»

> Nota relatore: dichiarare subito che il progetto è **sperimentale** e in
> evoluzione, per gestire le aspettative e invitare a contribuire.

---

## Sezione 1 — Che cosa sono gli open data (8', slide 3–9)

**Slide 3 — Definizione**
- «Dati che possono essere liberamente usati, riutilizzati e ridistribuiti da
  chiunque, al più con il vincolo di citarne la fonte e condividerli allo stesso
  modo» (Open Definition — opendefinition.org).
- I 3 pilastri: **disponibilità e accesso**, **riutilizzo e ridistribuzione**,
  **partecipazione universale** (nessuna discriminazione d'uso, nemmeno
  "non commerciale").

**Slide 4 — Cosa NON è un open data**
- Un PDF scansionato non è (facilmente) riutilizzabile.
- Una pagina web senza download.
- Un formato proprietario chiuso.
- Una licenza con restrizioni non compatibili con la Open Definition.

**Slide 5 — La "scala" delle 5 stelle di Tim Berners-Lee**
- ⭐ dati disponibili online, qualunque formato
- ⭐⭐ dati strutturati (es. Excel)
- ⭐⭐⭐ formati non proprietari e aperti (CSV, JSON, XML)
- ⭐⭐⭐⭐ URI permanenti per gli elementi
- ⭐⭐⭐⭐⭐ dati collegati (Linked Data) ad altri dataset

> Nota: AgID richiede **almeno 3 stelle** e raccomanda di puntare a 5 per i dati
> di maggiore interesse.

**Slide 6 — Formati e interoperabilità**
- CSV, JSON, XML, GeoJSON, RDF; API REST per i dati dinamici.
- Perché l'apertura conta: l'interoperabilità permette di **combinare** dataset
  diversi e costruire servizi nuovi (l'esempio della "Torre di Babele").

**Slide 7 — Esempi d'uso concreti**
- Trasporti: orari e fermate per app di mobilità.
- Ambiente: qualità dell'aria, aree verdi, spiagge.
- Trasparenza: bilancio, contratti, spese.
- Turismo: punti di interesse, eventi, strutture ricettive.
- Ricerca e giornalismo: analisi civiche e data journalism.

**Slide 8 — Chi ci guadagna**
- **Cittadini**: trasparenza e controllo della cosa pubblica.
- **Imprese e startup**: nuovi servizi, minor costo di accesso al dato.
- **PA**: efficienza interna, meno richieste di accesso formale, immagine.
- **Territorio**: narrazione dei dati locali, pianificazione.

**Slide 9 — Un esempio locale**
- Collegare subito al territorio: quali dati pubblica già la Liguria / Imperia.
- Anticipare che il progetto serve a rendere questi dati più facili da trovare e
  riusare.

---

## Sezione 2 — La normativa italiana ed europea (9', slide 10–16)

**Slide 10 — Il quadro europeo**
- Prima direttiva PSI: **2003/98/CE** (riutilizzo dell'informazione del settore
  pubblico), modificata dalla 2013/37/UE.
- **Direttiva (UE) 2019/1024** "Open Data Directive": sostituisce/abroga la
  2003/98/CE, introduce i **dati di elevato valore (HVD)** e i **dati dinamici**.
- Regolamento di esecuzione **(UE) 2023/138**: individua le serie di dati di
  elevato valore (geodati, ambiente, trasporti, statistiche, ecc.).

**Slide 11 — Il recepimento in Italia**
- **D.Lgs. 24 gennaio 2006, n. 36** — attuazione della direttiva PSI: la base
  del riutilizzo dei dati pubblici.
- **D.Lgs. 8 novembre 2021, n. 200** — recepisce la direttiva (UE) 2019/1024
  **modificando il D.Lgs. 36/2006**: formati aperti, gratuità di principio,
  tempi di risposta alle richieste (30 giorni lavorativi), dati di elevato valore.
- In vigore dal 15 dicembre 2021.

**Slide 12 — Trasparenza e Codice dell'Amministrazione Digitale**
- **D.Lgs. 14 marzo 2013, n. 33** "Riordino della disciplina su trasparenza":
  obblighi di pubblicazione per le PA locali (es. art. 9 → **catalogo dei dati,
  metadati e banche dati**).
- **D.Lgs. 7 marzo 2005, n. 82 (CAD)**: art. 52 (dati aperti e riutilizzo),
  art. 68 (sviluppo dei sistemi informativi), art. 71 (linee guida AgID).

**Slide 13 — Le linee guida AgID**
- **Linee guida recanti regole tecniche per l'apertura dei dati e il riutilizzo
  dell'informazione del settore pubblico** (AgID, determina n. 183/2023), emesse
  ai sensi dell'art. 12 del D.Lgs. 36/2006.
- Sostituiscono le precedenti linee guida 2016.
- Requisiti chiave: ≥ **3 stelle**, formati aperti, licenze esplicite, API per i
  dati dinamici, metadati conformi al profilo **DCAT-AP_IT**.

**Slide 14 — Metadati e catalogazione: DCAT-AP_IT**
- **DCAT** (Data Catalog Vocabulary) → profilo europeo **DCAT-AP** → profilo
  italiano **DCAT-AP_IT**.
- Ogni dataset descritto con titolo, descrizione, temi, titolare, frequenza di
  aggiornamento, distribuzioni, licenza.
- L'harvesting permette ai cataloghi di federarsi: comuni → regioni → **dati.gov.it** → portale europeo.

**Slide 15 — dati.gov.it e la federazione**
- **dati.gov.it** è il portale nazionale dei dati aperti (riferimento unico ex
  art. 1 comma 8, D.Lgs. 102/2015).
- Le Regioni svolgono spesso il ruolo di **aggregatori territoriali**.
- Per la Liguria esiste già un catalogo regionale basato su CKAN:
  `dati.regione.liguria.it`.

**Slide 16 — Licenze**
- **IODL 2.0** (Italian Open Data License, AgID).
- **CC BY 4.0**, **CC BY-SA 4.0**, **CC0 1.0**.
- Messaggio: per essere davvero open, la licenza deve essere **esplicita** e
  compatibile con la Open Definition. Nel nostro portale la licenza di default è
  **CC BY 4.0**.

---

## Sezione 3 — Il progetto Open Data Imperia (14', slide 17–26)

**Slide 17 — Obiettivi del progetto**
- Iniziativa di **Fablab Imperia APS**: un portale open data civico per il
  territorio, libero e replicabile.
- Rendere i dati locali **trovabili, riusabili e catalogati**.
- Automatizzare la raccolta dei dati da fonti online con codice Python schedulato.

**Slide 18 — Perché CKAN**
- Piattaforma open source (AGPL) per cataloghi di dati, usata da PA e governi.
- Catalogo, ricerca a faccette, organizzazioni, API, DataStore, harvesting,
  estensioni. Base solida invece di reinventare la ruota.

**Slide 19 — Architettura tecnica**
- Schema: `CKAN` ⟷ `Collectors` ⟷ sorgenti esterne (via API).
- Componenti Docker: **CKAN**, **PostgreSQL** (+ DataStore), **Solr**, **Redis**,
  **Datapusher**, container **collectors**.
- Immagine CKAN + estensione locale `ckanext-openimperia`; hook di init automatico.

> Mostrare il diagramma di `docs/architecture.md`.

**Slide 20 — Il portale oggi (personalizzazione)**
- Branding **Open Data Imperia** (logo, tema, home).
- Lingua italiana, organizzazione **Fablab Imperia APS**.
- Licenze italiane + default **CC BY 4.0**.
- Sito volutamente **vuoto**: lo popoleremo con i collector.
- Demo: `http://localhost:5000`.

**Slide 21 — I collector: l'idea**
- Classi Python che **estraggono** dati da fonti online, li **normalizzano** e li
  **pubblicano** su CKAN via Action API.
- Nessun accesso diretto al database: si usa l'API → architettura pulita e
  stabile agli aggiornamenti.
- Esecuzione **schedulata** (cron) per mantenere i dati aggiornati.

**Slide 22 — Anatomia di una sorgente**
- Classe che eredita da `DataSource`:
  - `fetch()` → scarica i dati grezzi
  - `transform(raw)` → restituisce un `Dataset` (titolo, note, tag, risorse)
  - `validate()` / `run(dry_run)` → pubblica o simula
- **Autodiscovery**: basta aggiungere un file in `collectors/sources/`.
- Comandi: `python -m collectors --list`, `--source`, `--all`, `--dry-run`.

**Slide 23 — Il client CKAN**
- `CKANClient.upsert_dataset()` usa `package_show` + `package_create/update`.
- Idempotente: rieseguire un collector aggiorna, non duplica.
- Configurazione via variabili d'ambiente (URL + API key), segreti non nel repo.

**Slide 24 — Opzionale (se c'è tempo): codice dal vivo**
- Mostrare `collectors/core/collector.py` e `collectors/sources/example.py`.
- Menzionare la separazione `core/` (framework) e `sources/` (sorgenti).

**Slide 25 — Roadmap: le fonti dati per Imperia**
- **Regione Liguria** — harvesting del catalogo CKAN `dati.regione.liguria.it`.
- **ISTAT** — popolazione e statistiche comunali via API SDMX.
- **MIMIT** — prezzi carburanti (CSV ufficiale), filtrati per provincia di Imperia.
- **OpenStreetMap / Overpass** — punti di interesse del comune.
- **Metadati DCAT-AP_IT** e harvesting verso `dati.gov.it`.

**Slide 26 — Licenza e riuso del progetto**
- Codice **AGPL-3.0-or-later**: libero, modificabile, con obbligo di condivisione
  delle modifiche se esposto come servizio.
- Dati con licenza aperta (default CC BY 4.0).
- Invito: altri comuni e gruppi possono partire da questa base.

---

## Sezione 4 — Demo live (4', slide 27)

**Slide 27 — Demo**
Sequenza suggerita (preparare i comandi in anticipo, stack già avviato):

```bash
# 1) Avvio dello stack
docker compose up --build -d
docker compose ps

# 2) La home page personalizzata
#    aprire http://localhost:5000

# 3) L'organizzazione creata automaticamente
curl -s http://localhost:5000/api/3/action/organization_list

# 4) Elenco collector disponibili
PYTHONPATH=. python -m collectors --list

# 5) Un collector in dry-run (non pubblica nulla)
PYTHONPATH=. python -m collectors --source example --dry-run
```

Punti da far notare durante la demo:
- Branding, italiano, organizzazione e licenze.
- API CKAN documentata (`/api/3/action/...`).
- `dry-run` per testare senza pubblicare.
- Il sito parte **vuoto**: il popolamento è lo step successivo.

> Piano B: se la rete o Docker non funzionano, avere screenshot / video brevi
> oppure usare record delle pagine.

---

## Sezione 5 — Conclusioni e domande (3' + Q&A, slide 28–30)

**Slide 28 — Cosa abbiamo visto**
- Open data: definizione, 5 stelle, valore.
- Normativa: direttiva UE, D.Lgs. 36/2006 e 200/2021, D.Lgs. 33/2013, CAD,
  linee guida AgID, DCAT-AP_IT, dati.gov.it.
- Un caso concreto: CKAN + collector Python per Imperia, con licenza libera.

**Slide 29 — Come contribuire / riutilizzare**
- Codice e istruzioni su (repository GitHub del progetto).
- Prossimi passi: implementare i collector, esporre DCAT-AP_IT, test e dati reali.
- Contatti / mailing list / canale della community locale.

**Slide 30 — Grazie / domande**
- QR code al repository e al portale.
- Ringraziamento a Linux Day e agli organizzatori.

---

## Domande frequenti (preparare le risposte)

- **È obbligatorio per legge? Prima devo 2006, poi 2013, poi 2021: sintesi.** Sì,
  le PA hanno obblighi di pubblicazione e riutilizzo; le linee guida AgID danno le
  regole tecniche.
- **Open data = dati personali?** No: i dati personali sono esclusi o anonimizzati;
  il tema privacy (GDPR) è sempre da valutare.
- **Quale licenza scegliere?** CC BY 4.0 come default, IODL 2.0 per il contesto
  italiano; evitare licenze "non commerciali".
- **Quanto costa un portale così?** Solo infrastruttura: software tutto open
  source e gratuito.
- **Perché CKAN e non altro?** Maturità, ecosistema, conformità DCAT, harvesting.
- **Chi mantiene i dati aggiornati?** I collector schedulati + eventuale
  pubblicazione manuale dall'ente.
- **Potete usarlo per altri comuni?** Sì: è pensato per essere replicabile.

---

## Riferimenti (per la slide finale o la dispensa)

- Open Definition — https://opendefinition.org/od/2.1/it/
- Direttiva (UE) 2019/1024 (Open Data Directive) — EUR-Lex
- D.Lgs. 24 gennaio 2006, n. 36 (riutilizzo informazioni del settore pubblico)
- D.Lgs. 8 novembre 2021, n. 200 (recepimento direttiva UE 2019/1024)
- D.Lgs. 14 marzo 2013, n. 33 (trasparenza)
- D.Lgs. 7 marzo 2005, n. 82 — Codice dell'Amministrazione Digitale (CAD)
- AgID — Linee guida per l'apertura dei dati e il riutilizzo dell'informazione
  del settore pubblico (det. n. 183/2023)
- Linee guida per i cataloghi dati — profilo DCAT-AP_IT (docs.italia.it)
- Portale nazionale dei dati aperti — https://www.dati.gov.it/
- Catalogo Open Data Regione Liguria — https://dati.regione.liguria.it/
- CKAN — https://ckan.org/

---

## Note logistiche e materiali

- **Slide**: tema semplice e ad alto contrasto (leggibilità in aula). Una idea
  per slide.
- **Fonti immagini/icone**: usare solo risorse con licenza libera (es. set icone
  CC0); citare le fonti.
- **Backup demo**: video registrato dello stack funzionante + screenshot.
- **Handout**: QR code al repo e al portale; eventuale volantino con la scaletta.
- **Timing**: tenere d'occhio il minutaggio; la sezione 3 è quella che può
  sforare, la 1 e la 2 sono più "raccontabili".
