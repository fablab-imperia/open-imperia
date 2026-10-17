#!/usr/bin/env bash
#
# Smoke test del portale Open Data Imperia.
# Usa solo curl (e python3 per il parsing JSON). Non richiede dipendenze extra.
#
# Uso:
#   BASE_URL=http://localhost:5000 ./scripts/smoke-test.sh
#
# Opzionale (test di scrittura, crea e cancella un dataset di prova):
#   CKAN_API_KEY=<token-sysadmin> ./scripts/smoke-test.sh
#
set -uo pipefail

BASE_URL="${BASE_URL:-http://localhost:5000}"
EXPECTED_ORG="${EXPECTED_ORG:-fablab-imperia-aps}"
EXPECTED_TITLE="${EXPECTED_TITLE:-Open Data Imperia}"
CKAN_API_KEY="${CKAN_API_KEY:-}"

PASS=0
FAIL=0

BODY=""
HTTP_STATUS=""

ok()   { printf '  \033[32mPASS\033[0m %s\n' "$1"; PASS=$((PASS + 1)); }
bad()  { printf '  \033[31mFAIL\033[0m %s\n' "$1"; FAIL=$((FAIL + 1)); }
info() { printf '\n== %s ==\n' "$1"; }

# http_get <url> [curl args...] -> imposta $BODY e $HTTP_STATUS (nessuna subshell)
http_get() {
    local url="$1"; shift
    HTTP_STATUS=$(curl -s -o /tmp/oi-smoke-body -w '%{http_code}' "$@" "$url")
    BODY=$(cat /tmp/oi-smoke-body)
}

json_field() {
    printf '%s' "$BODY" | python3 -c "import sys,json; d=json.load(sys.stdin); print($1)" 2>/dev/null
}

info "Stato del portale"
http_get "$BASE_URL/api/3/action/status_show"
if [ "$HTTP_STATUS" = "200" ] && [ "$(json_field "d['success']")" = "True" ]; then
    ok "API status_show risponde (HTTP 200, success=true)"
else
    bad "API status_show non risponde correttamente (HTTP $HTTP_STATUS)"
fi

info "Home page"
http_get "$BASE_URL/"
if [ "$HTTP_STATUS" = "200" ]; then
    ok "Home raggiungibile (HTTP 200)"
else
    bad "Home non raggiungibile (HTTP $HTTP_STATUS)"
fi
if printf '%s' "$BODY" | grep -q "$EXPECTED_TITLE"; then
    ok "Il titolo '$EXPECTED_TITLE' è presente"
else
    bad "Titolo '$EXPECTED_TITLE' non trovato nella home"
fi

info "Organizzazioni"
http_get "$BASE_URL/api/3/action/organization_list"
if printf '%s' "$BODY" | grep -q "\"$EXPECTED_ORG\""; then
    ok "L'organizzazione '$EXPECTED_ORG' esiste"
else
    bad "L'organizzazione '$EXPECTED_ORG' non trovata"
fi

info "Licenze"
http_get "$BASE_URL/api/3/action/license_list"
if printf '%s' "$BODY" | grep -q '"cc-by"'; then
    ok "La licenza 'cc-by' è registrata"
else
    bad "La licenza 'cc-by' non è registrata"
fi

info "Risorse statiche"
for asset in "/css/openimperia.css" "/images/openimperia-logo.svg"; do
    http_get "$BASE_URL$asset"
    if [ "$HTTP_STATUS" = "200" ]; then
        ok "Asset servito: $asset"
    else
        bad "Asset non servito ($HTTP_STATUS): $asset"
    fi
done

info "Scrittura (dataset di prova)"
if [ -z "$CKAN_API_KEY" ]; then
    printf '  \033[33mSKIP\033[0m CKAN_API_KEY non impostata: salto il test di scrittura\n'
else
    NAME="smoke-test-$(date +%s)"
    HTTP_STATUS=$(curl -s -o /tmp/oi-smoke-body -w '%{http_code}' \
        -X POST "$BASE_URL/api/3/action/package_create" \
        -H "Authorization: $CKAN_API_KEY" -H "Content-Type: application/json" \
        -d "{\"name\":\"$NAME\",\"title\":\"Smoke test\",\"owner_org\":\"$EXPECTED_ORG\"}")
    BODY=$(cat /tmp/oi-smoke-body)
    LICENSE=$(json_field "d['result']['license_id']")
    if [ "$LICENSE" = "cc-by" ]; then
        ok "Licenza di default applicata automaticamente (cc-by)"
    else
        bad "Licenza di default non applicata (HTTP $HTTP_STATUS, trovato: '$LICENSE')"
    fi
    curl -s -X POST "$BASE_URL/api/3/action/package_delete" \
        -H "Authorization: $CKAN_API_KEY" -H "Content-Type: application/json" \
        -d "{\"id\":\"$NAME\"}" >/dev/null
    ok "Dataset di prova eliminato"
fi

printf '\n----------------------------------------\n'
printf 'Risultato: %d PASS, %d FAIL\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
