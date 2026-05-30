from abc import ABC, abstractmethod


class BaseEvaluator(ABC):
    """Base interface for evaluators."""

    @abstractmethod
    def evaluate(self, predictions, references):
        raise NotImplementedError
        