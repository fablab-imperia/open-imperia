import os
import re
import time
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
        self._datapusher_wait_disabled = False

    @classmethod
    def from_environment(cls):
        return cls(
            os.environ["CKAN_URL"],
            os.environ["CKAN_API_KEY"],
            int(os.getenv("COLLECTOR_HTTP_TIMEOUT", "60")),
        )

    def action(self, name: str, payload: dict):
        endpoint = urljoin(self.base_url, f"api/3/action/{name}")
        for attempt in range(2):
            try:
                response = self.session.post(
                    endpoint,
                    json=payload,
                    timeout=self.timeout,
                )
                break
            except requests.ConnectionError:
                self.session.close()
                if attempt == 1:
                    raise
                time.sleep(1)
        response.raise_for_status()
        result = response.json()
        if not result.get("success"):
            raise RuntimeError(f"CKAN action failed: {result}")
        return result["result"]

    def package_show(self, name: str):
        return self.action("package_show", {"id": name})

    def wait_for_datapusher(self, resource_id: str, timeout: int = 120):
        if self._datapusher_wait_disabled:
            return None
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                result = self.action(
                    "datapusher_status", {"resource_id": resource_id}
                )
            except requests.HTTPError:
                return None
            except requests.RequestException:
                self.session.close()
                time.sleep(1)
                continue
            status = result.get("status")
            if status in ("complete", "error"):
                return status
            time.sleep(1)
        self._datapusher_wait_disabled = True
        return None

    def upload_resource(self, package_id: str, resource: dict, existing=None):
        """Create or replace a CKAN resource and upload its CSV contents."""
        csv_content = resource["csv_content"]
        filename = re.sub(r"[^A-Za-z0-9._-]+", "-", resource["name"]).strip("-")
        if not filename.lower().endswith(".csv"):
            filename += ".csv"

        payload = {
            key: value
            for key, value in resource.items()
            if key != "csv_content" and value is not None
        }
        payload["package_id"] = package_id
        if existing:
            payload["id"] = existing["id"]
            action = "resource_update"
        else:
            action = "resource_create"

        endpoint = urljoin(self.base_url, f"api/3/action/{action}")
        # Drop any idle keep-alive connection before the upload: uWSGI may
        # close pooled connections between the metadata calls and this
        # multipart request, which surfaces as RemoteDisconnected. Forcing a
        # fresh connection avoids reusing a socket the server already closed.
        self.session.close()
        response = self.session.post(
            endpoint,
            data=payload,
            files={"upload": (filename, csv_content.encode("utf-8"), "text/csv")},
            headers={"Connection": "close"},
            timeout=self.timeout,
        )
        response.raise_for_status()
        result = response.json()
        if not result.get("success"):
            raise RuntimeError(f"CKAN action failed: {result}")
        uploaded = result["result"]
        self.wait_for_datapusher(uploaded["id"])
        return uploaded

    def upsert_dataset(self, dataset: Dataset):
        uploaded_resources = [
            resource for resource in dataset.resources if "csv_content" in resource
        ]
        payload = {
            "name": dataset.name,
            "title": dataset.title,
            "notes": dataset.notes,
            "tags": dataset.tags,
            "extras": dataset.extras,
            # Collector datasets are open data and must be publicly visible.
            "private": False,
        }
        # Upload file resources separately as multipart requests. Include any
        # metadata-only resources in package_create for compatibility.
        metadata_resources = [
            {key: value for key, value in resource.items() if key != "csv_content"}
            for resource in dataset.resources
            if "csv_content" not in resource
        ]

        org = os.getenv("CKAN_ORGANIZATION")
        if org:
            payload["owner_org"] = org

        try:
            existing_package = self.package_show(dataset.name)
        except requests.HTTPError as exc:
            if exc.response is None or exc.response.status_code != 404:
                raise
            if metadata_resources:
                payload["resources"] = metadata_resources
            package = self.action("package_create", payload)
            existing_resources = []
        else:
            # package_update replaces the resource list, deleting resources
            # that are not included in the payload. package_patch leaves them
            # untouched, so the files uploaded below can update them safely.
            patch_payload = {"id": existing_package["id"], **payload}
            if existing_package.get("state") == "deleted":
                patch_payload["state"] = "active"
            package = self.action("package_patch", patch_payload)
            existing_resources = existing_package.get("resources", [])

        for resource in uploaded_resources:
            existing = next(
                (item for item in existing_resources if item.get("name") == resource["name"]),
                None,
            )
            self.upload_resource(package["id"], resource, existing=existing)

        return package
