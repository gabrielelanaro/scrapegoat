# This is the main learning process
from typing import List, Tuple

import numpy as np
from sklearn.ensemble import RandomForestClassifier

from modAL.models import ActiveLearner

from .dataset import BinaryDataset
from .diagnostics import Diagnostics
from .transforms import CandidateTransform
from .types import Candidate, LabeledData, LabelValue


def _label(labels: List[str], train_label: str):
    if train_label + ":t" in labels:
        return True
    if train_label + ":f" in labels or "ignore:t" in labels:
        return False

    return None


class LabelerProcess:
    def __init__(self, dataset: BinaryDataset):
        self._dataset = dataset

        # We need to extract the labels
        self._tf = tf = CandidateTransform()

        # Initialize the model
        self._model = RandomForestClassifier()

        _, X_train, y_train = dataset.labeled()
        self._learner = ActiveLearner(
            estimator=self._model, X_training=X_train, y_training=y_train
        )

    def show_predictions(self, d: Diagnostics):
        d.reset()
        X_unl, X_tf = self._dataset.unlabeled()

        predictions = self._model.predict_proba(X_tf)[:, 1]

        for i, c in enumerate(X_unl):
            if predictions[i] >= 0.5:
                d.draw_candidate(c, color="blue", width=2)

        X_lab, _, y = self._dataset.labeled()

        for i, c in enumerate(X_lab):
            if y > 0.5:
                d.draw_candidate(c, color="green")
            else:
                d.draw_candidate(c, color="red")

        return d.display()

    def query(self) -> Tuple[int, Candidate]:
        X, X_tf = self._dataset.unlabeled()

        q_ix, _ = self._learner.query(X_tf)
        ix = int(q_ix.squeeze())

        return ix, X[ix]

    def teach(self, ix: int, val: LabelValue):
        y = 1.0 if val == LabelValue.POS else 0.0

        X, X_tf = self._dataset.unlabeled()

        q_X = X_tf[ix].reshape(1, -1)

        self._learner.teach(q_X, np.array([y]))
        self._dataset.add_label(ix, val)

    def get_predictions(
        self, candidates: List[Candidate], threshold=0.5
    ) -> List[LabeledData]:
        X = self._dataset.apply_transform(candidates)
        predictions = self._model.predict_proba(X)[:, 1]

        labels = []
        for i, c in enumerate(candidates):
            label = LabelValue.POS if predictions[i] > threshold else LabelValue.NEG
            labels.append(
                LabeledData(
                    label_name=self._dataset.label_name,
                    value=label,
                    ref=c.ref,
                    remarks=["machine_generated"],
                )
            )

        return labels
