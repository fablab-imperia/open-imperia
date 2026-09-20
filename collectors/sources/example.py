from collectors.core.collector import DataSource
from collectors.core.models import Dataset


class ExampleSource(DataSource):
    name = "example"
    title = "Sorgente dimostrativa"

    def fetch(self):
        return [
            {"nome": "Imperia", "provincia": "Imperia", "regione": "Liguria"},
        ]

    def transform(self, raw_data):
        return Dataset(
            name="openimperia-example",
            title="Dataset dimostrativo OpenImperia",
            notes="Dataset usato per verificare il framework dei collector.",
            tags=[
                {"name": "imperia"},
                {"name": "open-data"},
                {"name": "demo"},
            ],
            extras=[
                {"key": "source", "value": "OpenImperia example collector"},
                {"key": "territory", "value": "Imperia"},
            ],
            resources=[],
        )
