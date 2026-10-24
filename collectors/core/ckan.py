import os
from urllib.parse import urljoin

import requests

from collectors.core.models import Dataset


class CKANClient:
    def __init__(self, base_url: str, api_key: str, timeout: int = 60):
        self.base_url = base_url.rstrip("/") + "/"
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Authorization": api_key})

    @classmethod
    def from_environment(cls):
        return cls(
            os.environ["CKAN_URL"],
            os.environ["CKAN_API_KEY"],
            int(os.getenv("COLLECTOR_HTTP_TIMEOUT", "60")),
        )

    def action(self, name: str, payload: dict):
        endpoint = urljoin(self.base_url, f"api/3/action/{name}")
        response = self.session.post(
            endpoint,
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        result = response.json()
        if not result.get("success"):
            raise RuntimeError(f"CKAN action failed: {result}")
        return result["result"]

    def package_show(self, name: str):
        return self.action("package_show", {"id": name})

    def upsert_dataset(self, dataset: Dataset):
        payload = {
                "name": dataset.name,
                "title": dataset.title,
                "notes": dataset.notes,
                "tags": dataset.tags,
                "extras": dataset.extras,
                "resources": dataset.resources,
            }

            org = os.getenv("CKAN_ORGANIZATION")
            if org:
                payload["owner_org"] = org

            try:
                self.package_show(dataset.name)
            except requests.HTTPError as exc:
                if exc.response is None or exc.response.status_code != 404:
                    raise
                return self.action("package_create", payload)

            return self.action("package_update", payload)