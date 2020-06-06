from scrapegoat.dataset import BinaryDataset
from scrapegoat import factories

from scrapegoat.transforms import CandidateTransform


def test_dataset():
    candidates = [
        factories.candidate(),
        factories.candidate(path="HTML[1]/BODY[1]/DIV[2]"),
        factories.candidate(path="HTML[1]/BODY[1]/DIV[3]"),
    ]
    labels = [factories.labeled_data()]
    dataset = BinaryDataset(
        labels=labels,
        candidates=candidates,
        label_name="label",
        transform=CandidateTransform(),
    )

    X, _, y = dataset.labeled()

    assert X[0] == candidates[0]
    assert y[0] == True
