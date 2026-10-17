#!/usr/bin/env bash
#
# Genera il file `.env` di produzione a partire da `.env.prod.example`,
# sostituendo i "CHANGE_ME" con segreti casuali.
#
# Uso:
#   ./scripts/gen-prod-env.sh              # crea .env (fallisce se esiste)
#   ./scripts/gen-prod-env.sh --force      # sovrascrive .env esistente
#
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE="$ROOT_DIR/.env.prod.example"
TARGET="$ROOT_DIR/.env"

FORCE=0
[ "${1:-}" = "--force" ] && FORCE=1

if [ ! -f "$TEMPLATE" ]; then
    echo "Errore: template non trovato: $TEMPLATE" >&2
    exit 1
fi

if [ -f "$TARGET" ] && [ "$FORCE" -ne 1 ]; then
    echo "Errore: $TARGET esiste già. Usa --force per sovrascrivere." >&2
    exit 1
fi

gen() { openssl rand -base64 32 | tr -d '/+=' | cut -c1-32; }

PG_PASS="$(gen)"
DB_PASS="$(gen)"
DS_PASS="$(gen)"
SECRET="$(openssl rand -base64 48 | tr -d '/+=' | cut -c1-48)"
ADMIN_PASS="$(gen)"

cp "$TEMPLATE" "$TARGET"
chmod 600 "$TARGET"

sed -i \
    -e "s|^POSTGRES_PASSWORD=.*|POSTGRES_PASSWORD=${PG_PASS}|" \
    -e "s|^CKAN_DB_PASSWORD=.*|CKAN_DB_PASSWORD=${DB_PASS}|" \
    -e "s|^DATASTORE_READONLY_PASSWORD=.*|DATASTORE_READONLY_PASSWORD=${DS_PASS}|" \
    -e "s|ckandbuser:CHANGE_ME@|ckandbuser:${DB_PASS}@|g" \
    -e "s|datastore_ro:CHANGE_ME@|datastore_ro:${DS_PASS}@|g" \
    -e "s|^CKAN___BEAKER__SESSION__SECRET=.*|CKAN___BEAKER__SESSION__SECRET=${SECRET}|" \
    -e "s|^CKAN_SYSADMIN_PASSWORD=.*|CKAN_SYSADMIN_PASSWORD=${ADMIN_PASS}|" \
    "$TARGET"

echo "Creato $TARGET con segreti generati (permessi 600)."
echo
echo "Da completare a mano:"
echo "  - CKAN_SITE_URL / SITE_ADDRESS  (dominio reale)"
echo "  - CKAN_API_KEY                  (dopo il primo avvio, per i collector)"
echo
echo "Password amministratore CKAN (utente ${CKAN_SYSADMIN_NAME:-ckan_admin}):"
echo "  ${ADMIN_PASS}"
