# Reuse Analysis: EarthVQA

## 1. Dataset Selected

For this reuse analysis, I selected EarthVQA, a remote-sensing visual question answering dataset. It is relevant to the DisasterM3 evaluation framework because it also combines remote-sensing imagery with natural-language questions and ground-truth answers.

From the EarthVQA repository, the dataset is organized around image folders, mask folders, and QA annotation files. The data preparation section shows separate folders such as `images_png`, `masks_png`, and QA files such as `Train_QA.json`, `Val_QA.json`, and `Test_QA.json`. The repository also lists semantic categories such as background, building, road, water, barren, forest, agriculture, and playground.

This makes EarthVQA a useful reference for thinking about how another remote-sensing QA dataset could be added to the DisasterM3 framework.

## 2. Reusable Design Pattern: Dataset Adapter for Images, Masks, and QA Files

Based on the EarthVQA repository structure, one reusable pattern is to keep image files, semantic mask files, and question-answer annotations separate, then use a dataset adapter to connect them during loading.

In the EarthVQA setup, the data preparation section shows separate folders for `images_png` and `masks_png`, along with QA annotation files such as `Train_QA.json`, `Val_QA.json`, and `Test_QA.json`. This suggests a clear separation between raw visual assets and text-based QA annotations.

This structure can be wrapped inside a dataset adapter. The adapter would hide EarthVQA-specific file names and folder structure from the rest of the framework. Instead of making the model runner or evaluator understand `Train_QA.json`, `images_png`, and `masks_png` directly, the dataset loader would convert each example into a common internal format.

For example, an EarthVQA-style sample could be represented as:

```python
{
    "id": "earthvqa_001",
    "dataset": "EarthVQA",
    "image": "path/to/image.png",
    "question": "How many buildings are in this area?",
    "ground_truth": "3",
    "task": "counting",
    "metadata": {
        "mask": "path/to/mask.png",
        "split": "train"
    }
}
```

The important idea is not that every dataset must have the exact same files. Rather, each dataset adapter should translate its own structure into a standard sample format that the rest of the framework can use.

## 3. How This Fits the DisasterM3 Framework

In the project architecture, EarthVQA would fit into the dataset-loading stage:

```text
Dataset -> Model Runner -> Evaluator -> Experiment Tracker
```

An `EarthVQADataset` class could implement the same base interface as `DisasterM3Dataset`:

```python
class EarthVQADataset(BaseDataset):
    def load(self):
        ...
```

The loader would read EarthVQA QA files, connect each question-answer pair to the correct image, and optionally include the mask path as metadata. After this step, the model runner would only need to receive a standard sample containing an image, question, and task type. It would not need to know the original EarthVQA folder layout.

This design also helps the evaluator. For example:

- if the task is general VQA, the evaluator can use exact-match or normalized answer accuracy;
- if the task is counting, the evaluator can use absolute error or mean absolute error;
- if semantic masks are useful for a future task, they can be passed through metadata without changing the model runner.

## 4. Why This Pattern Is Useful

This pattern is useful because DisasterM3 and EarthVQA do not have the same dataset structure. DisasterM3 uses its own subset JSON files and image path fields, while EarthVQA uses image folders, mask folders, and separate QA JSON files.

Without dataset adapters, adding EarthVQA would likely require editing the main execution script and adding dataset-specific branches. With adapters, the dataset-specific parsing stays inside `EarthVQADataset`, while the rest of the framework can continue using the same model runner, evaluator, and experiment tracker.

This supports the main goal of the internship project, which is moving from dataset-specific scripts toward a reusable evaluation framework.

## 5. Summary

The EarthVQA repository structure provides a useful reference for handling remote-sensing VQA data, where image files, mask files, and QA annotations are organized separately and can be connected through a dataset adapter. This pattern would fit naturally into the DisasterM3 framework by allowing EarthVQA to be added as another dataset module without changing the model execution or evaluation logic.
