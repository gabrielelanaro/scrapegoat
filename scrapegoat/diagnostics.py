# A diagnostic tool

from pathlib import Path
from typing import List

from IPython.display import display
from PIL import Image, ImageDraw

from .types import Candidate


class Diagnostics:
    def __init__(self, screenshot_path: Path):
        self._path = screenshot_path
        self._backup = Image.open(self._path)
        self._im = self._backup.copy()

    def reset(self):
        self._im = self._backup.copy()

    def draw_candidates(self, candidates: List[Candidate], color: str = "red"):
        for c in candidates:
            self.draw_candidate(c, color=color)
        return self

    def draw_candidate(self, cand: Candidate, color: str = "red"):
        im = self._im
        draw = ImageDraw.Draw(im)

        draw.rectangle(
            xy=(cand.rect.left, cand.rect.top, cand.rect.right, cand.rect.bottom),
            outline=color,
        )
        return self

    def crop_candidate(self, cand: Candidate, color: str = "red", pad=0):
        self.reset()
        self.draw_candidate(cand, color)
        self._im = self._im.crop(
            (
                cand.rect.left - pad,
                cand.rect.top - pad,
                cand.rect.right + pad,
                cand.rect.bottom + pad,
            )
        )
        return self

    def display(self):
        return display(self._im)


def show_box(box, im):
    rect = box["rect"]
    draw = ImageDraw.Draw(im)
    # TODO: unclear why this is not the right position
    offset = 0
    draw.rectangle(
        xy=(
            rect["left"] + offset,
            rect["top"] + offset,
            rect["right"] + offset,
            rect["bottom"] + offset,
        ),
        outline="red",
    )
    r
