# Beyond the Submission Tasks

This file documents additional work completed beyond the required submission tasks and bonus points, motivated by a genuine interest in the project and an early attempt to preview the modular framework described in the internship.

## 1. Comparative Dataset Analysis (`related_work.md`)

A side-by-side comparison of DisasterM3, EarthVQA, and MONITRS covering the tasks they support, their annotation formats, evaluation metrics, and gaps. The goal was to understand the broader landscape before diving into implementation.

## 2. YAML Configuration System (`configs/`, `scripts/run_from_config.py`)

A YAML-driven launcher that addresses the configuration limitation identified in `analysis.md`. Dataset, model, and runtime settings can now be defined in one place without editing Python code. It wraps `run_vllm.py` without modifying it, preserving full backward compatibility. Example usage:

```bash
python scripts/run_from_config.py --config configs/disasterm3_qwen_example.yaml
```

## 3. Evaluation Layer (`evaluation/base.py`, `evaluation/vqa.py`, `evaluation/__init__.py`, `scripts/evaluate_vqa.py`)

One of the clearest limitations of the original repository is that it stops at generating raw model responses with no scoring or metric computation. To address this, a basic but complete evaluation layer was implemented across four files.

`evaluation/base.py` defines a `BaseEvaluator` abstract class that establishes a standard `evaluate(predictions, references)` interface for all future task-specific evaluators. `evaluation/vqa.py` implements `VQAEvaluator` on top of this base class, with answer normalization (lowercasing, punctuation removal, whitespace cleaning) and exact-match accuracy scoring. `evaluation/__init__.py` exposes both classes cleanly. `scripts/evaluate_vqa.py` provides a runnable entry point that loads prediction and reference files and prints a full accuracy report.

Together these four files close the inference-to-evaluation gap in the current codebase and directly preview the evaluation layer that the internship framework requires.
