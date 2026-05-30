import argparse
import subprocess
from pathlib import Path

import yaml


def add_optional_arg(command, name, value):
    if value is not None:
        command.extend([name, str(value)])


def main():
    parser = argparse.ArgumentParser(description="Run DisasterM3 inference from a YAML config.")
    parser.add_argument("--config", required=True, help="Path to YAML config file.")
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    dataset = config.get("dataset", {})
    model = config.get("model", {})
    runtime = config.get("runtime", {})

    script_path = runtime.get("script", "pyscripts/run_vllm.py")

    command = [
        "python",
        script_path,
        "--model_id",
        model["model_id"],
        "--subset",
        dataset["subset"],
    ]

    add_optional_arg(command, "--max_tokens", model.get("max_tokens"))
    add_optional_arg(command, "--batch_size", model.get("batch_size"))
    add_optional_arg(command, "--image_size", runtime.get("image_size"))
    add_optional_arg(command, "--tensor_parallel_size", runtime.get("tensor_parallel_size"))

    if runtime.get("overwrite", False):
        command.append("--overwrite")

    print("Running command:")
    print(" ".join(command))

    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
    