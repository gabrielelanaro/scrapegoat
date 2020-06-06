from scrapegoat import factories
from scrapegoat.dataset import BinaryDataset
from scrapegoat.labeler import LabelerProcess
from scrapegoat.transforms import CandidateTransform
from scrapegoat.types import LabelValue


def test_labeler():
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
    labeler = LabelerProcess(dataset)

    ix, c = labeler.query()
    labeler.teach(ix, LabelValue.NEG)
