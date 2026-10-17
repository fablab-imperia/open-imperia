# Deploy in produzione (VPS IONOS, Debian 13, 4 GB RAM)

Guida passo-passo per portare Open Data Imperia online con `docker-compose.prod.yml`
e HTTPS automatico tramite Caddy.

Dominio previsto: **dati.fablabimperia.org**.

---

## 1. Prerequisiti sul VPS

Accedi via SSH come utente con privilegi `sudo`. Sistema aggiornato:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl ca-certificates
```

### 1.1 Swap (consigliato con 4 GB)

CKAN + Solr + PostgreSQL possono avvicinarsi al limite di RAM: 2 GB di swap
evitano il kill dei processi da parte dell'OOM killer.

```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
free -h
```

### 1.2 Docker Engine + Compose

```bash
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker "$USER"
newgrp docker
docker --version
docker compose version
```

### 1.3 Firewall

Solo SSH, HTTP e HTTPS devono essere raggiungibili. Caddy userà le porte 80/443
(la 80 serve anche al rinnovo dei certificati).

```bash
sudo apt install -y ufw
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo ufw status
```

> Se usi il firewall del pannello IONOS, apri lì le stesse porte (22, 80, 443)
> e chiudi tutto il resto.

---

## 2. DNS

Nel DNS di `fablabimperia.org` crea un record di tipo **A**:

| Nome | Tipo | Valore          | TTL  |
|------|------|-----------------|------|
| dati | A    | `<IP-del-VPS>`  | 300  |

Verifica che risolva (può servire qualche minuto):

```bash
dig +short dati.fablabimperia.org
```

Deve restituire l'IP del VPS. **Caddy ottiene il certificato TLS solo dopo che il
DNS punta al server.** Se non hai ancora accesso al DNS, salta al §4
("Test senza DNS") e torna qui dopo.

---

## 3. Deploy

### 3.1 Clona il repository

```bash
sudo mkdir -p /opt/openimperia && sudo chown "$USER" /opt/openimperia
git clone https://github.com/fablab-imperia/open-imperia.git /opt/openimperia
cd /opt/openimperia
```

### 3.2 Crea il file `.env` con i segreti

Lo script genera password e segreti casuali a partire dal template:

```bash
./scripts/gen-prod-env.sh
```

Controlla e completa a mano i valori specifici del dominio:

```bash
nano .env
```

Assicurati che siano corretti:

```ini
CKAN_SITE_URL=https://dati.fablabimperia.org
SITE_ADDRESS=dati.fablabimperia.org
ACME_EMAIL=fablabimperia@gmail.com
```

Annota la password di `ckan_admin` stampata dallo script.

### 3.3 Avvia lo stack

```bash
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml ps
```

Il primo avvio compila l'immagine CKAN, inizializza il database e crea
l'organizzazione `Fablab Imperia APS`. Attendi che `ckan` risulti `healthy`:

```bash
docker compose -f docker-compose.prod.yml logs -f ckan
```

### 3.4 Verifica

```bash
BASE_URL=https://dati.fablabimperia.org ./scripts/smoke-test.sh
```

Il portale è online su **https://dati.fablabimperia.org**.

---

## 4. Test senza DNS (opzionale)

Per provare lo stack prima che il DNS sia pronto, imposta in `.env`:

```ini
SITE_ADDRESS=:80
CKAN_SITE_URL=http://<IP-del-VPS>
```

Poi `docker compose -f docker-compose.prod.yml up -d caddy` e apri
`http://<IP-del-VPS>`. Quando il DNS è attivo, ripristina i valori reali e
ricrea Caddy:

```bash
docker compose -f docker-compose.prod.yml up -d --force-recreate caddy
```

---

## 5. Token API per i collector

I collector pubblicano su CKAN via API e richiedono un token.

### 5.1 Utente dedicato (consigliato)

```bash
DC="docker compose -f docker-compose.prod.yml"
$DC exec ckan ckan -c /srv/app/ckan.ini user add collector password=ScegliUnaPassword email=collector@fablabimperia.org
```

Aggiungi `collector` come editor dell'organizzazione: accedi al portale come
`ckan_admin` → pagina dell'organizzazione **Fablab Imperia APS** → *Manage* →
*Members* → aggiungi `collector` con ruolo **Editor**.

### 5.2 Genera il token e inseriscilo in `.env`

```bash
$DC exec ckan ckan -c /srv/app/ckan.ini user token add collector collectors
```

Copia il token in `.env`:

```ini
CKAN_API_KEY=<token-generato>
```

Infine ricrea il container dei collector:

```bash
$DC up -d --force-recreate collectors
```

---

## 6. Operazioni quotidiane

Tutte le operazioni si eseguono dalla directory `/opt/openimperia`:

```bash
DC="docker compose -f docker-compose.prod.yml"
```

### 6.1 Log

```bash
$DC logs -f ckan        # applicazione
$DC logs -f caddy       # accessi e certificati
$DC logs -f collectors  # raccolta dati
```

### 6.2 Aggiornamento del codice

```bash
cd /opt/openimperia
git pull
$DC up -d --build
```

### 6.3 Backup del database

```bash
mkdir -p ~/backup
$DC exec -T db pg_dump -U postgres ckandb | gzip > ~/backup/ckan-$(date +%F).sql.gz
$DC exec -T db pg_dump -U postgres datastore | gzip > ~/backup/datastore-$(date +%F).sql.gz
```

Per un backup automatico giornaliero, aggiungi una voce in `crontab -e`:

```cron
15 3 * * * cd /opt/openimperia && docker compose -f docker-compose.prod.yml exec -T db pg_dump -U postgres ckandb | gzip > /home/USER/backup/ckan-$(date +\%F).sql.gz
```

Vanno conservati anche i volumi Docker `ckan_storage` (file caricati) e i file
`.env` (segreti).

### 6.4 Ripristino

```bash
gunzip -c ~/backup/ckan-2026-10-17.sql.gz | $DC exec -T db psql -U postgres -d ckandb
```

---

## 7. Note su risorse e prestazioni

Il compose di produzione è già tarato per 4 GB:

- Solr con heap ridotto (`-Xms256m -Xmx768m`)
- PostgreSQL con parametri di memoria contenuti
- limiti di memoria per ogni container (`mem_limit`)

Se il VPS resta sotto pressione, controlla con `docker stats` e `free -h`.
Aumentando la RAM si possono alzare `SOLR_JAVA_MEM` e i `mem_limit`.

---

## 8. Risoluzione dei problemi

- **Caddy non ottiene il certificato**: il DNS non punta ancora al VPS, oppure
  le porte 80/443 sono chiuse. Controlla `$DC logs caddy` e `dig +short <dominio>`.
- **`ckan` non diventa `healthy`**: controlla `$DC logs ckan`; spesso è un
  problema di connessione a `db`/`solr` o di migrazioni.
- **Link o cookie con schema errato**: verifica che `CKAN_SITE_URL` usi `https://`
  e ricrea il container `ckan`.
- **Collector non pubblicano**: verifica `CKAN_API_KEY` in `.env` e i log con
  `$DC logs collectors`.
