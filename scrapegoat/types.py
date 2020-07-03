from dataclasses import asdict, dataclass, field, replace
from enum import Enum, unique
from typing import Dict, Generic, List, Optional, TypeVar

from selenium.webdriver.remote.webelement import WebElement


@dataclass
class Rect:
    """A rectangle"""

    top: float
    left: float
    bottom: float
    right: float

    @property
    def height(self):
        return self.bottom - self.top

    @property
    def width(self):
        return self.right - self.left


@dataclass
class Candidate:
    rect: Rect
    text: str
    tag: str
    path: str
    url: str
    style: Dict
    node: Optional[WebElement] = None

    @property
    def ref(self):
        return self.url + self.path

    def serialize(self):
        return asdict(replace(self, node=None))

    @classmethod
    def from_dict(cls, data):
        return cls(**{**data, "rect": Rect(**data["rect"])})


@unique
class LabelValue(Enum):
    POS = "t"
    NEG = "f"


T = TypeVar("T")


@dataclass
class LabeledData:
    label_name: str
    value: LabelValue
    ref: str
    remarks: List[str] = field(default_factory=list)

    def serialize(self):
        return asdict(replace(self, value=self.value.value))

    @classmethod
    def from_dict(cls, data):
        return cls(**{**data, "value": LabelValue(data["value"])})


@unique
class PULabelType(Enum):
    POS = LabelValue.POS.value
    NEG = LabelValue.NEG.value
    UNK = "u"


@dataclass(frozen=True)
class LinkType:
    source: str
    target: str
    value: PULabelType
    linkName: str = ""
    remarks: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data):
        return cls(**{**data, "value": PULabelType(data["value"])})

    def serialize(self):
        return asdict(replace(self, value=self.value.value))
