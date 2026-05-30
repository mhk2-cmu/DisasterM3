import string

from .base import BaseEvaluator


class VQAEvaluator(BaseEvaluator):
    """Simple exact-match evaluator for VQA-style outputs."""

    def normalize_answer(self, text):
        text = str(text).lower().strip()
        text = text.translate(str.maketrans("", "", string.punctuation))
        text = " ".join(text.split())
        return text

    def evaluate(self, predictions, references):
        reference_by_id = {item["id"]: item for item in references}

        total = 0
        correct = 0
        details = []

        for pred in predictions:
            sample_id = pred["id"]

            if sample_id not in reference_by_id:
                continue

            prediction = pred.get("response", pred.get("prediction", ""))
            reference = reference_by_id[sample_id].get("ground_truth", "")

            norm_pred = self.normalize_answer(prediction)
            norm_ref = self.normalize_answer(reference)

            is_correct = norm_pred == norm_ref

            total += 1
            correct += int(is_correct)

            details.append(
                {
                    "id": sample_id,
                    "prediction": prediction,
                    "ground_truth": reference,
                    "correct": is_correct,
                }
            )

        accuracy = correct / total if total > 0 else 0.0

        return {
            "metric": "exact_match_accuracy",
            "total": total,
            "correct": correct,
            "accuracy": accuracy,
            "details": details,
        }
        