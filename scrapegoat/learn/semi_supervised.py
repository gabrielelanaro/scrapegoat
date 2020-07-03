# We do a semi-supervised / unlabeled transductive thing. Let's get started
import numpy as np
from typing import Optional, NamedTuple
from sklearn.datasets import make_classification
from sklearn.base import BaseEstimator, clone


class SSEnsembleParams(NamedTuple):
    n_samples: int = 100
    n_estimators: int = 100
    random_state: Optional[int] = None


def train_ss_ensemble(
    clf: BaseEstimator,
    params: SSEnsembleParams,
    X: np.ndarray,
    y: np.ndarray,
    lb_mask: np.ndarray,
):
    rng = np.random.RandomState(params.random_state)

    # We want to return out of bag predictions
    ulb_mask = ~lb_mask

    # TODO: not really necessary but we could set them all to zero from the outside as well
    y = y.copy()

    y[ulb_mask] = 0
    ulb_indices = ulb_mask.nonzero()[0]

    y_oob_sum = np.zeros(len(y))
    y_oob_hit = np.zeros(len(y))

    for i in range(params.n_estimators):
        bag_ulb_indices = rng.choice(ulb_indices, size=params.n_samples)
        bag_lb_indices = lb_mask.nonzero()[0]

        bag_indices = np.concatenate([bag_ulb_indices, bag_lb_indices])

        X_bag = X[bag_indices]
        y_bag = y[bag_indices]

        oob_mask = np.ones(len(y), dtype="bool")
        oob_mask[bag_indices] = False

        X_oob = X[oob_mask]

        clf = clone(clf)
        clf.fit(X_bag, y_bag)

        y_oob = clf.predict_proba(X_oob)
        y_oob_sum[oob_mask] += y_oob[:, 1]
        y_oob_hit[oob_mask] += 1

    return y_oob_sum / y_oob_hit
