# Evaluation Methodology for Vision-Language Models

Vision-Language Models (VLMs) are evaluated by testing how well they can use both visual and textual information to produce correct, relevant, and useful outputs. In disaster analysis from remote sensing data, this often means giving the model a satellite or aerial image together with a natural-language question or instruction, then comparing the model's response against a ground-truth answer or annotation.

## 1. Nature of Evaluation Data

Evaluation data for VLMs usually contains paired visual and textual information. A single example may include:

- an image, such as a satellite image before or after a disaster,
- a text prompt or question,
- a ground-truth answer, label, or annotation,
- optional metadata, such as disaster type, location, sensor type, or time.

Depending on the task, the ground truth may take different forms, such as a class label, a short answer, a bounding box, a segmentation mask, a count, or a reference description.

In this project context, datasets such as DisasterM3, EarthVQA, and MONITRS fit this pattern because they combine remote-sensing imagery with task-specific labels, questions, or annotations for disaster analysis. A typical example might pair a post-disaster image with the question "How many damaged buildings are visible?" where the expected answer could be a number, a class label, or a short text response.

## 2. Model Inputs and Outputs

The model input usually consists of an image and a text prompt. The output format depends on the task:

- Visual Question Answering (VQA): short answers such as "yes", "flood", or "three buildings"
- Classification: a category label such as "damaged" or "intact"
- Captioning / report generation: a free-text description or summary of the image
- Multi-turn reasoning: a sequence of answers requiring consistency across related questions

Because VLMs can produce free-form text, evaluation often requires normalization before scoring. For example, answers may be converted to lowercase, punctuation may be removed, and equivalent responses like "yes" and "Yes." may be treated the same.

## 3. Common Evaluation Metrics

The choice of metric depends on the output type.

For classification tasks, common metrics include accuracy, precision, recall, and F1-score. These are useful when the model must choose from a fixed set of categories, such as disaster type or damage level.

For VQA tasks, exact match accuracy is commonly used when the expected answer is short or belongs to a fixed answer set. For more open-ended responses, text-similarity metrics may also be used. BLEU and ROUGE measure word or phrase overlap between the generated answer and the reference answer, while CIDEr is often used for caption-style evaluation by rewarding descriptions that match reference descriptions. BERTScore uses contextual embeddings to capture semantic similarity, which makes it more flexible when the model's wording differs from the reference. However, these metrics should be interpreted carefully because text similarity does not always guarantee factual correctness.

For detection and localization tasks, Intersection over Union (IoU) and mean Average Precision (mAP) measure whether predicted bounding boxes match ground-truth locations across classes and confidence thresholds.

For segmentation tasks, mean IoU and Dice coefficient compare predicted pixel-level regions with ground-truth masks.

For counting tasks, mean absolute error (MAE) compares predicted counts with true values.

## 4. Challenges in VLM Evaluation

Several challenges arise when evaluating VLMs, especially in disaster and remote sensing domains:

- Language ambiguity: More than one answer may be valid, so exact-match metrics can underestimate model quality.
- Benchmark bias: A model may exploit dataset patterns, such as frequent yes/no answers, without truly understanding the image.
- Hallucination: VLMs can generate plausible but incorrect responses that surface-level metrics may miss.
- Domain gap: Remote sensing images vary by sensor type, resolution, viewing angle, and conditions such as clouds or smoke, which can challenge general-purpose VLMs.
- Fine-grained reasoning: Disaster tasks often require subtle distinctions, such as damaged vs. intact buildings or flooded vs. dry roads.

Because of this, evaluation should not only report a single final score. Inspecting prediction examples, error cases, and performance by disaster type or task gives a more complete picture.

## 5. Reproducible Benchmarking

For systematic comparison, VLM evaluation should be reproducible. This means recording the dataset, model, task, prompt format, preprocessing steps, metrics, runtime, and prediction outputs. This is important because small changes in the prompt or input formatting can affect VLM outputs.

Experiment tracking tools such as MLflow or Weights & Biases help organize and compare results across runs. A modular evaluation framework should make it possible to switch datasets or models without rewriting evaluation code, enabling fairer comparison across different disaster benchmarks and model backends.

## Summary

VLM evaluation involves giving a model visual and textual inputs, collecting its predictions, comparing them with ground-truth annotations, and reporting task-appropriate metrics. For disaster analysis, the evaluation process should also be reproducible and flexible enough to compare different datasets, models, and task types.
