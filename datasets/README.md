# Dataset Adapters

This folder contains dataset adapters added for the modular evaluation framework.

## Files

- `base.py`: defines the shared `BaseDataset` interface.
- `disasterm3.py`: loads DisasterM3 subset JSON files.
- `earthvqa.py`: bonus adapter for EarthVQA QA annotation files.

## EarthVQA Adapter

The EarthVQA adapter was added for the bonus task of supporting one external dataset. It is based on the dataset organization described in the EarthVQA README and the loading pattern used in EarthVQA’s own `data/earthvqa.py` file.

The adapter expects a split-specific QA JSON file, connects each image name to its question-answer records, and returns examples with dataset metadata and stable IDs. This follows EarthVQA’s own loading pattern, where a QA JSON file maps image names to lists of question-answer items.
