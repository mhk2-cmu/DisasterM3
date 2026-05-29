# DisasterM3 Minimal Execution Notes

## 1. Goal

The goal of this task was to attempt a minimal execution of one DisasterM3 script and document the dependencies, execution steps, encountered issues, and reproducibility limitations.

The script selected for this attempt was:

```text
pyscripts/run_vllm.py
```

This script was selected because the repository README uses it as the benchmark inference entry point for running VLMs on DisasterM3 subsets.

## 2. Environment

The execution attempt was performed in Google Colab.

Observed environment:

```text
Python 3.12.13
```

GPU availability was checked using:

```bash
nvidia-smi
```

The command returned:

```text
/bin/bash: line 1: nvidia-smi: command not found
```

This indicates that the current Colab runtime did not have GPU access enabled or available.

## 3. Repository Setup

The forked repository was cloned using:

```bash
git clone https://github.com/mhk2-cmu/DisasterM3.git
```

After cloning, the working directory was:

```text
/content/DisasterM3
```

The repository contained:

```text
README.md
__init__.py
models/
pyscripts/
vision_tasks.md
evaluation_methodology.md
analysis.md
```

The main script was present at:

```text
pyscripts/run_vllm.py
```

## 4. Minimal Script Attempts

First, I tried to inspect the command-line interface:

```bash
python pyscripts/run_vllm.py --help
```

This failed with:

```text
ModuleNotFoundError: No module named 'vllm'
```

I then tried a README-style benchmark command from the repository root:

```bash
python pyscripts/run_vllm.py --model_id Qwen/Qwen2.5-VL-7B-Instruct --subset bearing_body
```

This also failed with the same error:

```text
ModuleNotFoundError: No module named 'vllm'
```

This confirms that the script cannot begin execution in the current environment until `vllm` is installed.

## 5. Dependencies Observed

From the imports in `pyscripts/run_vllm.py`, the script depends on packages including:

```text
Pillow
tqdm
transformers
vllm
```

The script also imports local model configuration code:

```python
from models import build_model_config, ModelConfig
```

I checked installed packages using:

```bash
pip show vllm transformers torch pillow tqdm
```

The output showed that `transformers`, `torch`, `pillow`, and `tqdm` were installed, but `vllm` was not found:

```text
WARNING: Package(s) not found: vllm
```

Based on `models/__init__.py`, additional dependencies used by the model configuration logic include:

```text
torch
torchvision
numpy
transformers
qwen_vl_utils
decord
```

Some of these dependencies, especially `vllm`, are GPU-oriented and may require a compatible CUDA environment.

## 6. Dataset Availability Check

The repository README provides a dataset access link, but the dataset files are not included directly in the GitHub repository clone. When I checked for a local `data/` directory using:

```bash
ls data
```

the command returned:

```text
ls: cannot access 'data': No such file or directory
```

This does not necessarily mean the dataset is unavailable. Rather, it means that the dataset must likely be requested or downloaded separately and then placed under the expected local directory structure. 

## 7. README Path Clarification

The README benchmark examples use a path like:

```bash
python disaster_m3/pyscripts/run_vllm.py --model_id Qwen/Qwen2.5-VL-7B-Instruct --subset bearing_body
```

In my cloned fork, the script is located at:

```text
pyscripts/run_vllm.py
```

Therefore, when running from inside the repository root, the command would be:

```bash
python pyscripts/run_vllm.py --model_id Qwen/Qwen2.5-VL-7B-Instruct --subset bearing_body
```

If the README assumes a parent directory or package folder named `disaster_m3`, the expected working directory should be clarified.

## 8. Encountered Issues

The minimal execution attempt revealed three main issues:

1. Missing dependency: `vllm` was not installed, causing both `--help` and the README-style benchmark command to fail before argument parsing or dataset loading.
2. Dataset not locally available: the cloned repository did not include the dataset files directly. The README links to a dataset access process, but I had not yet obtained and placed the dataset under the expected `data/` directory.
3. No GPU detected: `nvidia-smi` was not available in the current Colab runtime, which may prevent running large VLM inference even after installing dependencies.

## 9. Reproducibility Notes

To fully reproduce a DisasterM3 benchmark run, the following would be needed:

- documented installation commands for the required Python packages,
- access to a GPU-enabled environment compatible with `vllm`,
- downloaded DisasterM3 dataset files placed under the expected `data/` directory,
- clarification of the expected working directory and script path,
- a small sample command for testing the pipeline on a minimal subset.

I did not proceed with installing `vllm` in this runtime because the current Colab session did not expose a GPU through `nvidia-smi`, and the required DisasterM3 `data/` directory was also not locally available. Even if the dependency were installed, a full benchmark run would still require the dataset files and a compatible GPU/CUDA environment.

## 10. Suggested README Improvements

The README could be improved by adding:

- a `requirements.txt` or environment setup section,
- explicit dataset download/access and placement instructions,
- expected folder structure after dataset download,
- hardware/runtime notes for `vllm`,
- a minimal smoke-test command,
- clarification of whether the script should be run as `pyscripts/run_vllm.py` from the repository root or through another package/folder path.

## 11. Status

The script was partially executed. The repository was cloned successfully and the benchmark script was located, but full execution was blocked by the missing `vllm` dependency, lack of GPU availability in the current Colab runtime, and the fact that the DisasterM3 dataset had not yet been downloaded or placed under the expected local `data/` directory.
