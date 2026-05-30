# Related Work: Comparative Overview of Disaster-Focused Remote Sensing VLM Benchmarks

DisasterM3, EarthVQA, and MONITRS all sit at the intersection of remote sensing and vision-language understanding, but they approach the problem from meaningfully different angles. Understanding what each one covers, and what each one leaves out, is useful groundwork for thinking about what a unified evaluation framework needs to handle.

---

## Side-by-Side Comparison

| | **DisasterM3** | **EarthVQA** | **MONITRS** |
|---|---|---|---|
| Focus | Post-disaster damage assessment | Urban/rural scene understanding for city planning | Temporal monitoring of disaster progression |
| Images | 26,988 bi-temporal pairs (optical + SAR) | 6,000 single-time images | ~10,000 event sequences (Sentinel-2) |
| QA pairs | 123,010 | 208,593 | 44,308 train / 10,196 test |
| Disaster types | 10 types, 36 events, 5 continents | Not disaster-specific | FEMA-declared US disasters (hurricanes, floods, fires, etc.) |
| Sensors | Optical + SAR | High-res optical only (WorldView-3) | Optical only (Sentinel-2, 10m) |
| Temporal | Bi-temporal (pre/post) | Single timestamp | Multi-image sequences over event duration |
| Tasks | 9 tasks across recognition, counting, segmentation, report generation | Judging, counting, object situation analysis, comprehensive analysis | Event classification, temporal grounding, location grounding |
| Annotation source | Domain experts (FEMA/UNOSAT guidelines) | Manual + ArcGIS-assisted | FEMA records + LLM-processed news articles |
| Evaluation metrics | Accuracy (MCQ), GPT-4.1 scoring (reports), cIoU/mIoU (segmentation) | Accuracy, RMSE (counting) | Accuracy (MCQ), BLEU/ROUGE/METEOR (open-ended), LLM-as-judge |
| Models benchmarked | 14 VLMs (open-source, commercial, RS-specific) | 8 general + 2 RS VQA methods | 3 models (VideoLLaVA, TEOChat, Gemini 2.0-flash) |

---

## What Each Paper Does Well

DisasterM3 is the most comprehensive in terms of task diversity and disaster coverage. The inclusion of SAR imagery is a meaningful design choice rather than just an add-on, since cloud cover during disasters makes optical-only evaluation unrealistic. The 9-task taxonomy progresses logically from simple recognition to full report generation, which makes it a strong foundation for a multi-task eval framework. Benchmarking 14 models also gives a solid sense of where the field currently stands.

EarthVQA is less about disasters specifically and more about relational reasoning over complex scenes. Its strength is in the depth of its QA design, where questions are tied to actual city planning needs and require reasoning about spatial relationships between multiple objects, not just identifying what is present. The proposed SOBA framework and the numerical difference loss also address a concrete weakness in how counting tasks are typically evaluated, which is worth keeping in mind for the evaluation layer of the framework.

MONITRS fills a gap neither of the other two address, which is tracking how a disaster unfolds over time. Rather than comparing a before and after snapshot, it captures the full progression of an event through sequences of satellite images paired with news-derived captions. The data pipeline itself is a contribution, using LLMs to geolocate events from news articles and generate temporally-aligned captions, which is a practical approach to a dataset that would be extremely expensive to annotate manually.

---

## Gaps and What They Mean for a Unified Framework

Looking across all three, a few gaps stand out.

None of them share a common evaluation protocol. DisasterM3 uses GPT-4.1 as a judge for open-ended tasks, MONITRS uses BLEU/ROUGE and an LLM judge, and EarthVQA uses accuracy and RMSE. A framework that wants to run the same model across all three cannot simply reuse the same evaluator, the evaluation layer needs to be task-aware and dataset-aware at the same time.

The datasets also load very differently. DisasterM3 is built around bi-temporal image pairs with rich per-sample metadata, EarthVQA pairs images with semantic masks and structured QA sets, and MONITRS provides variable-length sequences with news article captions. A naive unified data loader would break on at least one of these, so the dataset abstraction layer needs to handle different input modalities, temporal structures, and annotation formats without forcing any of them into an awkward common schema.

Cross-dataset evaluation is not something any of these papers attempt. Each evaluates models on its own benchmark only, which means there is no baseline for cross-dataset generalization, arguably the most practically useful thing a unified framework could provide.

Finally, MONITRS is the only one that deals with temporal sequences of more than two images, which introduces a model requirement the other two do not have. Not all VLMs can handle variable-length image sequences, so model compatibility becomes a real constraint the framework needs to manage explicitly.

---

These gaps are essentially the design requirements for what this project aims to build, a dataset abstraction layer flexible enough to handle three structurally different input formats, an evaluation layer with task-specific logic, and an experiment tracking setup that makes cross-dataset and cross-model comparison systematic rather than ad hoc.
