# Immagine che esegue i collector OpenImperia su base cron.
#
# Al primo avvio lancia subito un update (i dati per la demo sono visibili
# immediatamente), poi programma le esecuzioni secondo
# COLLECTOR_CRON_SCHEDULE (formato cron standard, default: ogni ora).

FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/openimperia

RUN apt-get update \
    && apt-get install -y --no-install-recommends cron \
    && rm -rf /var/lib/apt/lists/*

COPY collectors/ /opt/openimperia/collectors/
COPY scripts/ /opt/openimperia/scripts/
COPY docker/collectors/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh /opt/openimperia/scripts/*.sh \
    && pip install --no-cache-dir -r /opt/openimperia/collectors/requirements.txt

CMD ["/entrypoint.sh"]