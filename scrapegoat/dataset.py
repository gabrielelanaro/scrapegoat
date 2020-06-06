from typing import List

import numpy as np

from .types import Candidate, LabeledData, LabelValue
from .transforms import CandidateTransform


class BinaryDataset:
    def __init__(
        self,
        candidates: List[Candidate],
        labels: List[LabeledData],
        label_name: str,
        transform: CandidateTransform,
    ):
        self._dataset = candidates
        self.label_name = label_name
        self._tf = transform
        self._labels = labels[:]

        # Transformed dataset
        self._tf_dataset = np.array([self._tf.encode(d) for d in self._dataset])

        # We need to extract the labels
        self._labels_by_ref, self._labeled, self._pool = self._build_labeled_unlabeled_arrays(
            labels, label_name
        )

    def labeled(self):
        return (
            [self._dataset[i] for i in self._labeled],
            self._tf_dataset[self._labeled],
            np.array([self._binary_label(ix) for ix in self._labeled]),
        )

    def unlabeled(self):
        return (
            [self._dataset[i] for i in self._pool],
            np.array(self._tf_dataset[self._pool]),
        )

    def add_label(self, unlabeled_index: int, val: LabelValue):
        candidate = self._dataset[self._pool[unlabeled_index]]
        self._labeled.append(unlabeled_index)
        self._labels_by_ref[candidate.ref] = val
        self._labels.append(
            LabeledData(label_name=self.label_name, value=val, ref=candidate.ref)
        )
        self._pool.pop(unlabeled_index)

    def pop_label(self, index=None) -> LabeledData:
        lab = self._labels.pop(index)
        self._labels_by_ref, self._labeled, self._pool = self._build_labeled_unlabeled_arrays(
            self._labels, self.label_name
        )

        return lab

    def labels(self) -> List[LabeledData]:
        return self._labels[:]

    def _build_labeled_unlabeled_arrays(
        self, labels: List[LabeledData], label_name: str
    ):
        # Small utility function to build the data structure containing the binary labels

        # We need to extract the labels
        labels_by_ref = {l.ref: l.value for l in labels if l.label_name == label_name}

        labeled = [i for i, d in enumerate(self._dataset) if d.ref in labels_by_ref]
        pool = [i for i, d in enumerate(self._dataset) if d.ref not in labels_by_ref]

        return labels_by_ref, labeled, pool

    def _binary_label(self, ix):
        return float(self._labels_by_ref[self._dataset[ix].ref] == LabelValue.POS)
