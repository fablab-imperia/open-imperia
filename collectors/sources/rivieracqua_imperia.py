import csv
import re
from io import StringIO

from bs4 import BeautifulSoup
import requests

from collectors.core.collector import DataSource
from collectors.core.models import Dataset


def _clean_text(value):
    return " ".join(value.split())


def _truncate(value, limit=63):
    encoded = value.encode("utf-8")
    if len(encoded) <= limit:
        return value
    return encoded[:limit].decode("utf-8", "ignore").rstrip()


def _unique_names(names, limit=63):
    result = []
    used = set()
    for name in names:
        base = _truncate(name or "Punto", limit)
        candidate = base
        index = 2
        while candidate in used:
            suffix = f" ({index})"
            candidate = _truncate(base, limit - len(suffix)) + suffix
            index += 1
        used.add(candidate)
        result.append(candidate)
    return result


class RivieracquaImperiaSource(DataSource):
    name = "rivieracqua-imperia"
    title = "Qualità dell'acqua - Rivieracqua (Imperia)"

    URL = "https://rivieracqua.it/qualita-dell-acqua/"

    def fetch(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        resp = requests.get(self.URL, timeout=60, headers=headers)
        resp.raise_for_status()
        return resp.text

    def transform(self, raw_data):
        soup = BeautifulSoup(raw_data, "html.parser")
        zone_labels = {}
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if "#tab_" in href:
                panel_id = href.split("#", 1)[1]
                zone_labels.setdefault(
                    panel_id, _clean_text(link.get_text(" ", strip=True))
                )

        resources = []
        used_names = set()

        for index, table in enumerate(soup.find_all("table")):
            panel = table.find_parent("div", class_="panel")
            panel_id = panel.get("id", "") if panel else ""
            slug = panel_id[4:] if panel_id.startswith("tab_") else ""
            slug = re.sub(r"[^a-z0-9]+", "-", slug.lower()).strip("-")
            zone = (
                zone_labels.get(panel_id)
                or slug.replace("-", " ").title()
                or "Rivieracqua"
            )

            rows = []
            for tr in table.find_all("tr"):
                cells = [
                    _clean_text(td.get_text(" ", strip=True))
                    for td in tr.find_all(["td", "th"])
                ]
                if cells:
                    rows.append(cells)
            if not rows:
                continue
            if not any("PUNTI DI PRELIEVO" in cell.upper() for cell in rows[0]):
                continue

            params_index = next(
                (
                    i
                    for i, row in enumerate(rows)
                    if any(cell.upper().startswith("PARAMETRI") for cell in row)
                ),
                None,
            )
            if params_index is None:
                continue

            params_row = rows[params_index]
            unit_index = next(
                (i for i, cell in enumerate(params_row) if "UNITA" in cell.upper()),
                None,
            )
            limit_index = next(
                (
                    i
                    for i, cell in enumerate(params_row)
                    if "VALORI" in cell.upper() or "LIMITE" in cell.upper()
                ),
                None,
            )
            if unit_index is None or limit_index is None:
                continue

            value_end = min(unit_index, limit_index)
            value_indexes = list(range(1, value_end))
            if not value_indexes:
                continue

            point_names = []
            for i in value_indexes:
                name = rows[0][i] if i < len(rows[0]) else ""
                point_names.append(name or zone)
            point_names = _unique_names(point_names)

            data_rows = []
            for row in rows[params_index + 1 :]:
                if not row or not row[0]:
                    continue
                parameter = row[0]
                if parameter.upper().startswith("PARAMETRI"):
                    continue
                values = [row[i] if i < len(row) else "" for i in value_indexes]
                unit = row[unit_index] if unit_index < len(row) else ""
                limit = row[limit_index] if limit_index < len(row) else ""
                data_rows.append([parameter, *values, unit, limit])
            if not data_rows:
                continue

            output = StringIO(newline="")
            writer = csv.writer(output)
            writer.writerow(
                [
                    "Parametro",
                    *point_names,
                    "Unità di misura",
                    "Valore limite (D.Lgs 18/2023)",
                ]
            )
            writer.writerows(data_rows)
            csv_content = output.getvalue()

            base_name = f"qualita-acqua-{slug}" if slug else f"qualita-acqua-{index + 1}"
            resource_name = base_name
            suffix = 2
            while resource_name in used_names:
                resource_name = f"{base_name}-{suffix}"
                suffix += 1
            used_names.add(resource_name)

            resources.append(
                {
                    "name": resource_name,
                    "format": "CSV",
                    "mimetype": "text/csv",
                    "description": (
                        f"Qualità dell'acqua - {zone} "
                        f"(punti di prelievo: {', '.join(point_names)})"
                    ),
                    "csv_content": csv_content,
                }
            )

        return Dataset(
            name="qualita-acqua-imperia",
            title="Qualità dell'acqua - Comune di Imperia e zone rivierasche (Rivieracqua)",
            notes=(
                "Dati sulla qualità dell'acqua potabile forniti da Rivieracqua S.p.A. "
                "per l'ATO Ovest della provincia di Imperia. I valori sono riportati per "
                "punti di prelievo e parametri con riferimento ai limiti del D.Lgs 18/2023."
            ),
            tags=[
                {"name": "acqua"},
                {"name": "qualita-acqua"},
                {"name": "potabile"},
                {"name": "imperia"},
                {"name": "liguria"},
                {"name": "rivieracqua"},
            ],
            extras=[
                {"key": "source", "value": "https://rivieracqua.it/qualita-dell-acqua/"},
                {"key": "territory", "value": "Imperia"},
                {"key": "frequency", "value": "aggiornamento periodico"},
                {"key": "license", "value": "Dati pubblici forniti dal gestore"},
            ],
            resources=resources,
        )
