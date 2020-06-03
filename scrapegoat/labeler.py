# This is the main learning process
from collections import defaultdict
from typing import Dict, List

import numpy as np
from sklearn.ensemble import RandomForestClassifier

from modAL.models import ActiveLearner

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
    def __init__(
        self, dataset: List[Candidate], label_name: str, labels: List[LabeledData]
    ):
        self._dataset = dataset

        # We need to extract the labels
        self._labels = labels
        self._labels_by_ref = {
            l.ref: l.value for l in labels if l.label_name == label_name
        }

        self._label_name = label_name
        # True, Negative or None

        self._labeled = [
            i for i, d in enumerate(dataset) if d.ref in self._labels_by_ref
        ]
        self._pool = [
            i for i, d in enumerate(dataset) if d.ref not in self._labels_by_ref
        ]
        self._tf = tf = CandidateTransform()

        # Transformed dataset
        self._tf_dataset = np.array([tf.encode(d) for d in dataset])

        # Initialize the model
        self._model = RandomForestClassifier()

        self._learner = ActiveLearner(
            estimator=self._model,
            X_training=self._tf_dataset[self._labeled],
            y_training=np.array([self._binary_label(ix) for ix in self._labeled]),
        )

    def _binary_label(self, ix):
        return float(self._labels_by_ref[self._dataset[ix].ref] == LabelValue.POS)

    def show_predictions(self, d: Diagnostics):
        X_pool = self._tf_dataset[self._pool]

        predictions = self._model.predict_proba(X_pool)[:, 1]

        for i, ix in enumerate(self._pool):
            if predictions[i] >= 0.5:
                d.draw_candidate(self._dataset[ix], color="blue")

        for ix in self._labeled:
            if self._binary_label(ix) == LabelValue.POS:
                d.draw_candidate(self._dataset[ix], color="green")
            else:
                d.draw_candidate(self._dataset[ix], color="red")

        return d.display()

    def query(self):
        X_pool = self._tf_dataset[self._pool]
        q_ix, _ = self._learner.query(X_pool)

        return q_ix, self._dataset[self._pool[q_ix[0]]]

    def teach(self, ref, val: LabelValue):

        y = 1.0 if val == LabelValue.POS else 0.0
        ix = self._pool[int(ref[0])]

        q_X = self._tf_dataset[ix].reshape(1, -1)

        self._learner.teach(q_X, np.array([y]))

        c = self._dataset[ix]

        self._labeled.append(ix)
        self._labels_by_ref[c.ref] = val
        self._pool.remove(ix)

    def get_labeled(self) -> List[LabeledData]:
        labels = []
        for ix in self._labeled:
            c = self._dataset[ix]
            labels.append(
                LabeledData(
                    label_name=self._label_name,
                    value=self._labels_by_ref[c.ref],
                    ref=c.ref,
                )
            )

        return labels

    def get_predictions(
        self, candidates: List[Candidate], threshold=0.5
    ) -> List[LabeledData]:
        tf = self._tf
        X = np.array([tf.encode(d) for d in candidates])
        predictions = self._model.predict_proba(X)[:, 1]

        labels = []
        for i, c in enumerate(candidates):
            label = LabelValue.POS if predictions[i] > threshold else LabelValue.NEG
            labels.append(
                LabeledData(label_name=self._label_name, value=label, ref=c.ref)
            )

        return labels
