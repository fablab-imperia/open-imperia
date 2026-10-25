import csv
from io import StringIO

import requests

from collectors.core.collector import DataSource
from collectors.core.models import Dataset


def _clean_text(value):
    if value is None:
        return ""
    return " ".join(str(value).split())


def _value(block):
    if not isinstance(block, dict):
        return ""
    return _clean_text(block.get("valore", ""))


def _tempo_value(items, keyword):
    for item in items or []:
        if not isinstance(item, dict):
            continue
        label = _clean_text(item.get("etichetta", "")).lower()
        if keyword in label:
            return _clean_text(item.get("valore", ""))
    return ""


def _map_description(mappe, phase, kind):
    phase_data = mappe.get(phase) if isinstance(mappe, dict) else None
    if not isinstance(phase_data, dict):
        return ""
    item = phase_data.get(kind)
    if not isinstance(item, dict):
        return ""
    return _clean_text(item.get("descrizioneSimbolo", ""))


class ArpalMeteoImperiaSource(DataSource):
    name = "arpal-meteo-imperia"
    title = "Bollettino meteo - Comune di Imperia (ARPAL)"

    URL = (
        "https://www.arpal.liguria.it/contenuti_statici/"
        "bollettino_meteo/bollettino_liguria_comuni.json"
    )
    CODICE_ISTAT_IMPERIA = "008001"

    def fetch(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Accept": "application/json,*/*;q=0.8",
        }
        resp = requests.get(self.URL, timeout=60, headers=headers)
        resp.raise_for_status()
        return resp.json()

    def transform(self, raw_data):
        data_emissione = _clean_text(raw_data.get("dataEmissione", ""))
        comuni = raw_data.get("comuni") or []
        comune = next(
            (
                item
                for item in comuni
                if str(item.get("codiceIstat", "")).zfill(6)
                == self.CODICE_ISTAT_IMPERIA
            ),
            None,
        )
        if comune is None:
            raise ValueError(
                f"Comune di Imperia ({self.CODICE_ISTAT_IMPERIA}) non trovato "
                "nel bollettino ARPAL"
            )

        rows = []
        for previsione in comune.get("previsioni") or []:
            il_tempo = previsione.get("ilTempoA") or []
            mappe = previsione.get("mappe") or {}
            rows.append(
                [
                    _clean_text(previsione.get("dataPrevisione", "")),
                    data_emissione,
                    self.CODICE_ISTAT_IMPERIA,
                    _value(previsione.get("statoCielo")),
                    _value(previsione.get("temperature")),
                    _value(previsione.get("venti")),
                    _value(previsione.get("mare")),
                    _value(previsione.get("umidita")),
                    _value(previsione.get("segnalazioniProtCiv")),
                    _tempo_value(il_tempo, "minima"),
                    _tempo_value(il_tempo, "massima"),
                    _tempo_value(il_tempo, "precipitazioni"),
                    _map_description(mappe, "mattina", "statoCielo"),
                    _map_description(mappe, "mattina", "vento"),
                    _map_description(mappe, "pomeriggio", "statoCielo"),
                    _map_description(mappe, "pomeriggio", "vento"),
                    _map_description(mappe, "sera", "statoCielo"),
                    _map_description(mappe, "sera", "vento"),
                ]
            )

        output = StringIO(newline="")
        writer = csv.writer(output)
        writer.writerow(
            [
                "Data previsione",
                "Data emissione",
                "Codice ISTAT",
                "Stato del cielo",
                "Temperature",
                "Venti",
                "Mare",
                "Umidità",
                "Segnalazioni di Protezione Civile",
                "Temperatura minima",
                "Temperatura massima",
                "Probabilità di precipitazioni",
                "Mattina - Cielo",
                "Mattina - Vento",
                "Pomeriggio - Cielo",
                "Pomeriggio - Vento",
                "Sera - Cielo",
                "Sera - Vento",
            ]
        )
        writer.writerows(rows)

        return Dataset(
            name="bollettino-meteo-imperia",
            title="Bollettino meteo - Comune di Imperia (ARPAL)",
            notes=(
                "Previsioni meteo per il Comune di Imperia pubblicate da ARPAL "
                "(Agenzia Regionale per la Protezione dell'Ambiente Ligure). "
                "Il bollettino riporta le previsioni giornaliere con stato del "
                "cielo, temperature, venti, mare, umidità e indicazioni per "
                "Protezione Civile, oltre alle mappe di mattina, pomeriggio e sera. "
                f"Ultima emissione: {data_emissione or 'non disponibile'}."
            ),
            tags=[
                {"name": "meteo"},
                {"name": "previsioni-meteo"},
                {"name": "bollettino"},
                {"name": "arpal"},
                {"name": "imperia"},
                {"name": "liguria"},
            ],
            extras=[
                {"key": "source", "value": self.URL},
                {"key": "territory", "value": "Imperia"},
                {"key": "frequency", "value": "quotidiano"},
                {"key": "license", "value": "Dati pubblici forniti da ARPAL"},
                {"key": "data_emissione", "value": data_emissione},
            ],
            resources=[
                {
                    "name": "bollettino-meteo-imperia",
                    "format": "CSV",
                    "mimetype": "text/csv",
                    "description": (
                        "Previsioni meteo giornaliere per il Comune di Imperia "
                        "con dettagli per mattina, pomeriggio e sera."
                    ),
                    "csv_content": output.getvalue(),
                }
            ],
        )
