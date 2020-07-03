from typing_extensions import Protocol
from typing import TypeVar

Data = TypeVar("Data", contravariant=True)
Labels = TypeVar("Labels", covariant=True)


class PredictiveModel(Protocol[Data, Labels]):
    def predict(self, data: Data) -> Labels:
        ...
