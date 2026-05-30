# DisasterM3 Paper Summary 

--- 

## Problem Statement

Disasters cause massive damage to infrastructure and human life, and assessing that damage quickly matters a lot for rescue and recovery. Satellite imagery is already widely used for this. The rise of Vision-Language Models (VLMs) opened up new possibilities, since these models can look at an image and answer questions about it in natural language. 

The problem is that existing VLM datasets for remote sensing were built around general tasks like land-use classification or image captioning, not disaster response. The one disaster-specific dataset that existed (FloodNet) only covered Hurricane Harvey and had fairly simple tasks. So there was no proper way to train or evaluate VLMs on the kinds of questions that actually matter in a disaster, like what got destroyed, how much, where, and what should be done about it. 

--- 

## Solution: The DisasterM3 Dataset

To address this, the authors built DisasterM3, a dataset designed around three ideas they call the "three multis":

- Multi-hazard: It covers 36 real historical disaster events across 10 types (earthquakes, floods, wildfires, hurricanes, tsunamis, tornadoes, explosions, volcanoes, landslides, conflict) and 5 continents. The reasoning is that different disasters damage things in fundamentally different ways, so a model trained only on floods will likely fail on earthquakes or explosions.

- Multi-sensor: Optical satellite images are often blocked by clouds during and after disasters, which is exactly when imagery is needed the most. The dataset includes SAR imagery alongside optical for this reason, since SAR can see through those conditions. This is an important practical consideration that most prior datasets ignored.
  
- Multi-task: The dataset defines 9 tasks covering 5 types of capabilities, namely recognizing disaster type and affected structures, counting damaged buildings, estimating road damage area, pixel-level segmentation of damaged objects, and generating full disaster reports with restoration advice. This reflects the fact that real disaster response requires different kinds of information at different stages.

The dataset contains 26,988 image pairs (pre and post-disaster) and 123,010 question-answer pairs, annotated by domain experts using FEMA and UNOSAT guidelines.

--- 

## Experimentation

The authors tested 14 VLMs on the dataset, ranging from smaller open-source models (LLaVA, Kimi-VL) to larger ones (InternVL3-78B, Qwen2.5-VL-72B), remote sensing-specific models (GeoChat, TeoChat, EarthDial), and commercial ones (GPT-4o, GPT-4.1).

The main takeaway is that all of them struggled. Even the best zero-shot models only reached around 40% accuracy on multiple-choice questions, and performance dropped further on SAR images since VLMs have very little SAR data in their training. Counting damaged objects was also a consistent weak point across all models.

The more encouraging result came from fine-tuning. Four models were fine-tuned on DisasterM3, and the improvements were significant, which reached up to +10.4% on QA tasks and +40.8% on segmentation. Fine-tuned models also became more stable across different prompt phrasings, which suggests the dataset is genuinely teaching the models something about disaster understanding rather than just overfitting to the format.
