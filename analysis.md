# DisasterM3 Repository Analysis

## 1. Current Repository Structure

The current DisasterM3 repository is lightweight and focused on running benchmark inference for the DisasterM3 dataset. The main structure is:

```text
DisasterM3/
├── README.md
├── __init__.py
├── models/
│   └── __init__.py
└── pyscripts/
    ├── __init__.py
    └── run_vllm.py
```

The `README.md` introduces the benchmark and provides example commands for running supported Vision-Language Models (VLMs). The main execution logic appears to be in `pyscripts/run_vllm.py`, while `models/__init__.py` contains model-specific configuration classes for model families such as Qwen-VL, InternVL, and LLaVA.

Overall, the repository is practical for running the original DisasterM3 benchmark, but it is not yet organized as a general modular evaluation framework.

## 2. Code Organization Analysis

The main script, `pyscripts/run_vllm.py`, handles several responsibilities in one place:

- defining prompt templates for different DisasterM3 subsets,
- converting dataset examples into model messages,
- loading local image paths,
- resizing images when needed,
- batching examples,
- initializing the VLM through `vllm`,
- running inference,
- saving generated responses to result files.

This makes the script useful for the original benchmark, but it also means that dataset preparation, prompt construction, model execution, and output writing are closely connected.

The `models/__init__.py` file already provides a partial model abstraction. It defines a base `ModelConfig` class and model-specific classes such as `QwenVL`, `InternVL`, and `Llava`. These classes handle model-specific prompt formatting and chat-template conversion, which is a useful pattern because different VLMs require different input formats.

However, model selection is still handled through string checks in `build_model_config(...)`, such as checking whether the model ID contains `"qwen"`, `"intern"`, or `"llava"`. This works for the currently supported models, but adding a new model would require editing the model configuration file.

Additionally, `models/__init__.py` contains several image and video preprocessing utilities, such as `build_transform`, `dynamic_preprocess`, `load_video`, and `load_video_frame_np`. These functions support model input preparation, but they are not strictly model configuration logic. Moving shared preprocessing helpers into a dedicated `utils/` module would make the model configuration file easier to maintain and would allow the same utilities to be reused by other model runners.

## 3. Dataset Coupling and Generalization

The current implementation is strongly tied to DisasterM3. In `run_vllm.py`, the dataset is loaded from a local JSON file based on the selected subset:

```python
subset_json = join(f"{PROJECT_ROOT}/data", f"{args.subset}.json")
```

The script also expects DisasterM3-specific fields such as `pre_image_path`, `post_image_path`, `image_path`, `prompts`, `options_str`, and `option_str`. For several tasks, image paths are built from the local `data/images` directory.

Because of this, the current framework is not yet plug-and-play for other datasets. To add a dataset such as EarthVQA or MONITRS, the main script would likely need new loading logic, new field mappings, new prompt templates, and additional subset-specific branches.

## 4. Identified Limitations

The current repository is a useful starting point, but several limitations appear when considering a reusable modular framework:

1. **Dataset-specific loading:** Data loading is tied to DisasterM3 JSON files and local image paths.
2. **Prompt construction inside the main script:** Prompt templates are defined directly in `run_vllm.py`, making them harder to reuse or modify independently.
3. **Subset-specific branching:** The message-building logic branches based on DisasterM3 subset names, which may become difficult to maintain as more datasets and tasks are added.
4. **No separate evaluation layer:** The inspected execution script focuses on generating and saving raw model responses to JSONL/JSON files. It does not compute metrics or compare predictions against ground truth within the same pipeline. For a reusable benchmarking framework, scoring and metric computation should be implemented as a separate evaluation layer.
5. **No full configuration system:** The script uses command-line arguments, but there is no YAML-based configuration that defines the dataset, model, task, prompt, evaluation method, and tracking setup in one place.
6. **No integrated experiment tracker:** Results are saved as JSONL/JSON files, but there is no integration with MLflow or Weights & Biases for comparing experiments across datasets and models.

## 5. Proposed Modular Redesign

The project description already proposes a modular structure with separate folders for configurations, datasets, models, evaluation, experiments, and utilities. This structure is appropriate for addressing the limitations observed in the current DisasterM3 repository.

```text
framework/
├── configs/
├── datasets/
│   ├── base.py
│   ├── disasterm3.py
│   ├── earthvqa.py
│   └── monitrs.py
├── models/
│   ├── base.py
│   ├── qwen_runner.py
│   ├── internvl_runner.py
│   └── llava_runner.py
├── evaluation/
│   ├── base.py
│   ├── vqa.py
│   ├── classification.py
│   └── counting.py
├── experiments/
│   ├── runner.py
│   └── tracker.py
├── utils/
└── main.py
```

Following the core architecture principle from the project description, the redesigned framework should follow:

```text
Dataset -> Model Runner -> Evaluator -> Experiment Tracker
```

### Dataset abstraction

A base dataset interface could define a standard method:

```python
class BaseDataset:
    def load(self):
        raise NotImplementedError
```

Each dataset adapter would convert its original format into a common internal format. For example, `DisasterM3Dataset` would handle DisasterM3 JSON files and image paths, while `EarthVQADataset` would handle EarthVQA-specific files and fields.

A standardized sample could contain:

```python
{
    "id": "example_001",
    "images": ["path/to/pre.png", "path/to/post.png"],
    "question": "How many damaged buildings are visible?",
    "ground_truth": "3",
    "task": "counting",
    "metadata": {
        "dataset": "DisasterM3",
        "subset": "building_damage_counting"
    }
}
```

### Model execution interface

The existing `ModelConfig` class and `build_model_config(...)` function provide a useful starting point for the redesigned model abstraction. The current `get_prompt_from_question(...)` pattern already separates some model-specific prompt formatting from the main execution script. In the redesigned framework, this idea could be extended into a fuller `BaseModelRunner` interface with a standard `predict(sample)` method, while preserving the factory/registration idea for selecting model backends.

```python
class BaseModelRunner:
    def predict(self, sample):
        raise NotImplementedError
```

Each model runner would handle model-specific input formatting and inference. This would allow the evaluator to call a standard `predict(...)` method without depending on the details of Qwen-VL, InternVL, LLaVA, or another model.

### Evaluation structure

Evaluation should be separated from inference. After predictions are generated, task-specific evaluators should compare predictions with ground truth.

Examples include:

- `VQAEvaluator` for exact-match or normalized answer accuracy,
- `ClassificationEvaluator` for accuracy or F1-score,
- `CountingEvaluator` for absolute error or mean absolute error,
- `CaptioningEvaluator` for text-generation metrics where appropriate.

### Configuration and experiment tracking

A YAML-based configuration system would allow experiments to be changed without editing Python code. For example, the config could specify the dataset, subset, model ID, task, evaluation metric, output path, and tracking tool.

Experiment tracking with MLflow or Weights & Biases could record:

- dataset name,
- model name,
- task,
- prompt template,
- preprocessing settings,
- metrics,
- runtime information,
- prediction artifacts.

This would make it easier to compare experiments such as Qwen-VL on DisasterM3 versus InternVL on EarthVQA.

## 6. Summary

The DisasterM3 repository is a useful and compact benchmark implementation for running VLM inference on the DisasterM3 dataset. It already includes some helpful model abstraction through `ModelConfig` and model-specific classes. However, the current workflow is still closely tied to DisasterM3-specific subsets, file paths, prompt formats, and result-saving logic.

To support a reusable modular evaluation framework, the codebase should separate dataset loading, model execution, evaluation, configuration, and experiment tracking. This would make it easier to evaluate multiple VLMs across DisasterM3, EarthVQA, MONITRS, and other disaster-related remote sensing benchmarks in a consistent and reproducible way.
