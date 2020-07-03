"""Classical inductive learning interfaces"""
from typing import TypeVar
from typing_extensions import Protocol
from .predictive import PredictiveModel

Data = TypeVar("Data", contravariant=True)
InLabels = TypeVar("InLabels", contravariant=True)
OutLabels = TypeVar("OutLabels", covariant=True)


class InductiveLearner(Protocol[Data, InLabels, OutLabels]):
    def learn(self, data: Data, labels: InLabels) -> PredictiveModel[Data, OutLabels]:
        ...
