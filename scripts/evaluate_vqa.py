import argparse
import json

from evaluation import VQAEvaluator


def load_jsonl(path):
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Evaluate VQA predictions with exact match.")
    parser.add_argument("--predictions", required=True, help="Path to prediction JSONL file.")
    parser.add_argument("--references", required=True, help="Path to reference JSON file.")
    parser.add_argument("--output", default=None, help="Optional output JSON file.")
    args = parser.parse_args()

    predictions = load_jsonl(args.predictions)
    references = load_json(args.references)

    evaluator = VQAEvaluator()
    results = evaluator.evaluate(predictions, references)

    print(json.dumps(results, indent=2))

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()

    