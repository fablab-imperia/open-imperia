# ckanext-openimperia

Estensione CKAN per il portale Open Data Imperia. Contiene solo codice di
presentazione e personalizzazione: non modifica il core di CKAN né accede
direttamente al database.

## Funzionalità

- `IConfigurer` — registra le cartelle `templates/` e `public/`; applica i
  default di branding (titolo, descrizione, logo, testo introduttivo, lingua
  italiana) solo se l'opzione non è già personalizzata in `ckan.ini` o via
  variabili d'ambiente; imposta la lista licenze del portale.
- `IActions` — azione concatenata (`chained action`) `package_create` che
  assegna la licenza di default **CC BY 4.0** (`cc-by`) ai nuovi dataset.
- `IClick` — comando `openimperia init` che crea l'organizzazione di default
  `Fablab Imperia APS`.

## File

```text
ckanext/openimperia/
├── plugin.py                 # plugin CKAN
├── licenses_group.json       # elenco licenze del portale
├── public/
│   ├── css/openimperia.css   # tema grafico
│   └── images/openimperia-logo.svg
└── templates/
    ├── base.html             # carica il CSS su tutte le pagine
    ├── footer.html           # footer personalizzato
    └── home/index.html       # home page personalizzata
```

## Configurazione

Tutte le opzioni possono essere impostate in `ckan.ini` o tramite variabili
d'ambiente con prefisso `CKAN__` (es. `CKAN__SITE_TITLE`). I default
dell'estensione si applicano solo quando il valore coincide con quello di CKAN.
