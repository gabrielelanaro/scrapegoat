import enum
from dataclasses import dataclass
from operator import pos
from typing import List
import numpy as np

from sklearn.tree import DecisionTreeClassifier

from ..bagging_pu import BaggingClassifierPU
from ..transforms import CandidateTransform
from ..types import Candidate, LabelValue, LinkType
from .node_extraction import PULabelType
from .transductive import TransductiveModel
from .semi_supervised import SSEnsembleParams, train_ss_ensemble


@dataclass(frozen=True)
class ProbLink:
    link: LinkType
    p: float


@dataclass
class EdgeExtractionModel(TransductiveModel):
    n_estimators: int = 64
    max_features: float = 1.0
    max_samples: int = 100
    pos_thr: float = 0.5

    def learn(self, data: List[Candidate], labels: List[LinkType]) -> List[ProbLink]:
        tf = CandidateTransform()
        # First of all we extract all the features
        features = {c.path: tf.encode(c) for c in data}

        pos_links = {(l.source, l.target) for l in labels if l.value == PULabelType.POS}
        neg_links = {(l.source, l.target) for l in labels if l.value == PULabelType.NEG}
        labeled_links = pos_links | neg_links

        unl_links = []
        for c1 in data:
            for c2 in data:

                if c1.path == c2.path or (c1.path, c2.path) in labeled_links:
                    continue
                else:
                    unl_links.append((c1.path, c2.path))

        # Subtraction of the features
        X_links = list(pos_links) + list(neg_links) + unl_links
        X = np.array([features[s] - features[t] for s, t in X_links])
        y = np.array([1] * len(pos_links) + [0] * len(neg_links) + [0] * len(unl_links))

        clf = DecisionTreeClassifier(max_features="auto")

        lb_mask = np.zeros(len(y), dtype="bool")
        lb_mask[: len(pos_links) + len(neg_links)] = True

        n_unl = sum(~lb_mask)

        oob_pred = train_ss_ensemble(
            clf,
            SSEnsembleParams(
                n_estimators=self.n_estimators, n_samples=min(self.max_samples, n_unl)
            ),
            X,
            y,
            lb_mask,
        )

        ret = []
        for i, d in enumerate(oob_pred):
            s, t = X_links[i]
            ret.append(
                ProbLink(
                    link=LinkType(
                        source=s,
                        target=t,
                        value=PULabelType.POS if d > self.pos_thr else PULabelType.NEG,
                    ),
                    p=d,
                )
            )
        return ret
