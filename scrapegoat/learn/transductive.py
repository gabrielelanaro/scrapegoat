"""Transductive learning"""
from typing import TypeVar
from typing_extensions import Protocol
from enum import Enum, unique

Data = TypeVar("Data", contravariant=True)
InLabels = TypeVar("InLabels", contravariant=True)
OutLabels = TypeVar("OutLabels", covariant=True)


class TransductiveModel(Protocol[Data, InLabels, OutLabels]):
    def learn(self, data: Data, labels: InLabels) -> OutLabels:
        ...


@unique
class LabelType(Enum):
    POS = 1
    NEG = 0
    UNK = -1

