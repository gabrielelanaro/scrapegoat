"""Factories for testing"""

from functools import partial

from .types import Candidate, LabeledData, LabelValue, Rect

rect = partial(Rect, top=0.0, bottom=0.0, right=0.0, left=0.0)
candidate = partial(
    Candidate,
    rect=rect(),
    text="candidate",
    tag="A",
    path="/HTML[1]/BODY[1]",
    url="http://www.example.com",
    style={
        "background": {"color": "rgba(0, 0, 0, 0)"},
        "border": "0px none rgb(0, 0, 238)",
        "color": "rgb(0, 0, 238)",
        "font": {
            "family": '"Times New Roman"',
            "size": "16px",
            "style": "normal",
            "variant": "normal",
            "weight": "400",
        },
    },
    node=None,
)
labeled_data = partial(
    LabeledData,
    label_name="label",
    value=LabelValue.POS,
    ref=candidate().ref,
    remarks=[],
)
