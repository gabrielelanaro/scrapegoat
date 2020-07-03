"""Transformations for machine learning"""

import re
from typing import List

import numpy as np

from .types import Candidate, Rect


class CandidateTransform:
    def __init__(self):

        self._cat = OneHotTransform(
            [
                "A",
                "SPAN",
                "BUTTON",
                "DIV",
                "ARTICLE",
                "P",
                "SELECT",
                "FORM",
                "H1",
                "H2",
                "H3",
                "H4",
                "H5",
                "H6",
                "DD",
                "LI",
                "LL",
                "UL",
                "TABLE",
            ]
        )
        self._font_style = OneHotTransform(["normal", "italic"])

    def encode(self, candidate: Candidate):
        # Path features
        path_features = re.findall(r"\[(\d+)\]", candidate.path)
        path_features = [int(p) for p in path_features]
        path_features = ([0, 0, 0] + path_features)[-3:]
        feats = {
            "tag": self._cat.encode(candidate.tag),
            "font_size": float(candidate.style["font"]["size"].replace("px", "")),
            "font_weight": float(candidate.style["font"]["weight"]),
            "font_style": self._font_style.encode(candidate.style["font"]["style"]),
            "is_valid_rect": is_valid_rect(candidate.rect),
            "text": [len(candidate.text), "€" in candidate.text],
            "path": path_features,
            "periodic": periodic_features(candidate.rect),
        }

        return np.concatenate(
            [
                feats["tag"],
                [
                    feats["is_valid_rect"],
                    candidate.rect.left,
                    candidate.rect.top,
                    candidate.rect.right,
                    candidate.rect.bottom,
                    candidate.rect.width,
                    candidate.rect.height,
                    candidate.rect.height / (candidate.rect.width + 0.0001),
                    feats["font_size"],
                    feats["font_weight"],
                ],
                feats["path"],
                feats["font_style"],
            ]
        )


def periodic_features(rect: Rect):
    max_period = 800
    n_harmonics = 4

    feats = []
    for i in range(1, n_harmonics + 1):
        feats.extend(
            [
                np.sin(2 * np.pi * rect.top / (max_period ** (1 / i))),
                np.cos(2 * np.pi * rect.top / (max_period ** (1 / i))),
            ]
        )
    return feats


class OneHotTransform:
    def __init__(self, categories: List[str]):
        self._categories = categories
        self._n_cat = len(categories)
        self._catmap = {cat: i for i, cat in enumerate(categories)}
        self._invcatmap = {i: cat for i, cat in enumerate(categories)}

    def encode(self, input: str):
        ret = np.zeros(self._n_cat)
        val = self._catmap.get(input)
        if val is not None:
            ret[val] = 1
        return ret


def is_valid_rect(rect: Rect):
    return rect.width > 0 and rect.height > 0
