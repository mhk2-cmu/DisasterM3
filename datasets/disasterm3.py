import json
from pathlib import Path

from .base import BaseDataset

class DisasterM3Dataset(BaseDataset):
    """Loader for DisasterM3 subset JSON files."""

    def __init__(self, data_root, subset):
        self.data_root = Path(data_root)
        self.subset = subset

    def load(self):
        subset_file = self.data_root / f"{self.subset}.json"

        if not subset_file.exists():
            raise FileNotFoundError(f"Dataset file not found: {subset_file}")

        with open(subset_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        examples = []
        for i, item in enumerate(data):
            item = dict(item)
            item["id"] = f"{self.subset}_{i}"
            item["dataset"] = "DisasterM3"
            item["subset"] = self.subset
            examples.append(item)

        return examples

