#!/usr/bin/env bash
set -euo pipefail

SCHEDULE="${COLLECTOR_CRON_SCHEDULE:-0 * * * *}"

install -m 0644 /dev/null /etc/cron.d/openimperia
{
    echo "PATH=/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
    echo "${SCHEDULE} cd /opt/openimperia && /opt/openimperia/scripts/update-all.sh >> /proc/1/fd/1 2>&1"
} > /etc/cron.d/openimperia
crontab /etc/cron.d/openimperia

echo "[entrypoint] Primo update all'avvio (rimuovere se indesiderato)..."
cd /opt/openimperia
/opt/openimperia/scripts/update-all.sh \
    || echo "[entrypoint] Primo update fallito (atteso se CKAN non ancora pronto)."

echo "[entrypoint] Avvio cron con schedule: ${SCHEDULE}"
exec cron -f