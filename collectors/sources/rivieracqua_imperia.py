import csv
from io import StringIO

from bs4 import BeautifulSoup
import requests

from collectors.core.collector import DataSource
from collectors.core.models import Dataset


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
        resources = []

        # Find all tables that look like water quality tables
        for table in soup.find_all("table"):
            # Try to get context (preceding headers/list items)
            prev = table.find_previous(["h2", "h3", "h4", "strong", "b", "p"])
            context_text = ""
            if prev:
                context_text = prev.get_text(strip=True)

            # Look for area/comune names nearby
            # Also check tabs - look backwards for list items or links with comune names
            # Simple approach: look for "PUNTI DI PRELIEVO" header in table
            table_text = table.get_text()
            if "PUNTI DI PRELIEVO" not in table_text and "PARAMETRI" not in table_text:
                continue

            # Keep cells as values and let csv.writer quote delimiters,
            # quotes, and newlines correctly.
            rows = []
            for tr in table.find_all("tr"):
                cells = []
                for td in tr.find_all(["td", "th"]):
                    cells.append(" ".join(td.get_text(" ", strip=True).split()))
                if cells:
                    rows.append(cells)
            if not rows:
                continue

            output = StringIO(newline="")
            writer = csv.writer(output)
            writer.writerows(rows)
            csv_content = output.getvalue()

            # Determine a name for this table
            name = "qualita-acqua"
            if "Imperia" in context_text or "Imperia" in table_text:
                name = "qualita-acqua-imperia"
            elif "Levante" in context_text:
                name = "qualita-acqua-imperia-levante"
            elif "Ponente" in context_text:
                name = "qualita-acqua-imperia-ponente"
            elif "Centro" in context_text:
                name = "qualita-acqua-imperia-centro"

            resources.append(
                {
                    "name": name,
                    "format": "CSV",
                    "mimetype": "text/csv",
                    "description": context_text or "Tabella qualità dell'acqua - Rivieracqua",
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
