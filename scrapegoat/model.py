from typing_extensions import Protocol


class Estimator(Protocol):
    def fit(self, X, y):
        ...

    def predict(self, X):
        ...

    def predict_proba(self, X):
        ...


def train_model(transform, classifier):
    pass


class PredictiveModel:
    def __init__(self, transform, classifier):
        self._tf = transform
        self._cf = classifier

    def train(self, labels):
        pass

    # def active_learner(self):
    #     return ActiveLearner(
    #         estimator=self._model,
    #         X_training=self._tf_dataset[self._labeled],
    #         y_training=np.array([self._binary_label(ix) for ix in self._labeled]),
    #     )
