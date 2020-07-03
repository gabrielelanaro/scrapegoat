import enum
import math
from dataclasses import dataclass
from typing import List

from sklearn.tree import DecisionTreeClassifier

from ..bagging_pu import BaggingClassifierPU
from ..transforms import CandidateTransform
from ..types import Candidate, LabelValue, PULabelType
from .transductive import TransductiveModel


@dataclass(frozen=True)
class ProbLabel:
    label: PULabelType
    p: float


@dataclass
class NodeExtractionModel(
    TransductiveModel[List[Candidate], List[PULabelType], List[ProbLabel]]
):
    n_estimators: int = 64
    max_features: float = 1.0
    max_samples: int = 100
    pos_thr: float = 0.5

    def learn(
        self, data: List[Candidate], labels: List[PULabelType]
    ) -> List[ProbLabel]:
        tf = CandidateTransform()
        # First of all we need to predict if it is a node.
        # Then we need to predict the relationship between them

        X = [tf.encode(c) for c in data]
        y = [1 if l == PULabelType.POS else 0 for l in labels]

        clf = DecisionTreeClassifier(max_features="auto")

        model = BaggingClassifierPU(
            base_estimator=clf,
            n_estimators=self.n_estimators,
            max_features=self.max_features,
            max_samples=self.max_samples,
        )
        model.fit(X, y)

        out = []
        for i, d in enumerate(model.oob_decision_function_[:, 1]):
            if labels[i] != PULabelType.UNK:
                out.append(ProbLabel(labels[i], d))
            else:
                lbl = PULabelType.POS if d > self.pos_thr else PULabelType.NEG
                out.append(ProbLabel(lbl, d))

        return out
