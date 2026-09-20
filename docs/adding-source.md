# Aggiungere una sorgente

Creare un file in:

```text
collectors/sources/nome_sorgente.py
```

con una classe che eredita da `DataSource`:

```python
from collectors.core.collector import DataSource
from collectors.core.models import Dataset

class MySource(DataSource):
    name = "my-source"
    title = "La mia sorgente"

    def fetch(self):
        ...

    def transform(self, raw_data) -> Dataset:
        ...
```

Non è necessario modificare il registry: l'autodiscovery trova automaticamente
le classi presenti nei moduli sotto `collectors.sources`.

Test:

```bash
PYTHONPATH=. python -m collectors --list
PYTHONPATH=. python -m collectors --source my-source --dry-run
```
