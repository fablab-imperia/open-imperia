from abc import ABC, abstractmethod
import logging

from collectors.core.ckan import CKANClient
from collectors.core.models import Dataset


class DataSource(ABC):
    name: str = ""
    title: str = ""
    enabled: bool = True

    def __init__(self):
        self.log = logging.getLogger(f"collector.{self.name}")

    @abstractmethod
    def fetch(self):
        """Download raw data from the source."""
        raise NotImplementedError

    @abstractmethod
    def transform(self, raw_data) -> Dataset:
        """Transform source data into a CKAN dataset."""
        raise NotImplementedError

    def validate(self, dataset: Dataset):
        if not dataset.name:
            raise ValueError("Dataset name is required")
        if not dataset.title:
            raise ValueError("Dataset title is required")

    def run(self, dry_run: bool = False):
        raw = self.fetch()
        dataset = self.transform(raw)
        self.validate(dataset)

        if dry_run:
            self.log.info(
                "DRY RUN: %s (%s) with %d resources",
                dataset.title, dataset.name, len(dataset.resources)
            )
            return dataset

        client = CKANClient.from_environment()
        client.upsert_dataset(dataset)
        self.log.info("Published dataset %s", dataset.name)
        return dataset
