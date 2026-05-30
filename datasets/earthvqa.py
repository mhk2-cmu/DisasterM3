import json
from pathlib import Path

from .base import BaseDataset

class EarthVQADataset(BaseDataset):
    """Loader for EarthVQA QA annotation files."""

    def __init__(self, data_root, split="Train"):
        self.data_root = Path(data_root)
        self.split = split

    def load(self):
        qa_file = self.data_root / f"{self.split}_QA.json"
        image_dir = self.data_root / self.split / "images_png"
        mask_dir = self.data_root / self.split / "masks_png"

        if not qa_file.exists():
            raise FileNotFoundError(f"EarthVQA QA file not found: {qa_file}")

        with open(qa_file, "r", encoding="utf-8") as f:
            qa_data = json.load(f)

        examples = []
        count = 0

        for image_name, qa_list in qa_data.items():
            for qa in qa_list:
                values = list(qa.values())

                if len(values) < 3:
                    raise ValueError(f"Unexpected QA format for image {image_name}: {qa}")

                question_type = values[0]
                question = values[1]
                answer = values[2]

                example = {
                    "id": f"earthvqa_{self.split.lower()}_{count}",
                    "dataset": "EarthVQA",
                    "split": self.split,
                    "image_path": str(image_dir / image_name),
                    "question_type": question_type,
                    "question": question,
                    "ground_truth": answer,
                    "raw": qa,
                }

                if mask_dir.exists():
                    example["mask_path"] = str(mask_dir / image_name)

                examples.append(example)
                count += 1

        return examples

  
