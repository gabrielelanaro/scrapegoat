import hashlib
import json
from pathlib import Path
from typing import List

from .types import Candidate, LabeledData


class Store:
    def __init__(self, store_dir):
        self.dir = Path(store_dir)
        if not self.dir.exists():
            self.dir.mkdir()

        self._index_path = self.dir / "index.json"
        self._index = {}

        if self._index_path.exists():
            with self._index_path.open() as f:
                self._index = json.load(f)

    def get_or_create_page(self, url):
        path = self.dir / _hash(url)
        if not path.exists():
            path.mkdir()

        self._index[url] = {"path": str(path.relative_to(self.dir))}
        self._flush_index()
        return Page(self, path)

    def _flush_index(self):
        with self._index_path.open("w") as f:
            json.dump(self._index, f)


def _hash(text: str) -> str:
    m = hashlib.sha256()
    m.update(text.encode())
    return m.hexdigest()


class Page:
    def __init__(self, store: Store, path: Path):
        self._store = store
        self._path = path

    @property
    def screenshot_path(self) -> Path:
        return self._path / "screenshot.png"

    @property
    def candidates_path(self) -> Path:
        return self._path / "candidates.json"

    @property
    def labels_path(self) -> Path:
        return self._path / "labels.json"

    def save_candidates(self, candidates: List[Candidate]):
        with (self.candidates_path).open("w") as f:
            json.dump([c.serialize() for c in candidates], f, sort_keys=True, indent=2)

    def get_candidates(self):
        with self.candidates_path.open() as f:
            candidates = json.load(f)

        return [Candidate.from_dict(c) for c in candidates]

    def save_labels(self, labels: List[LabeledData]):
        # We can save the binary labels
        with self.labels_path.open("w") as f:
            json.dump([l.serialize() for l in labels], f, sort_keys=True, indent=2)

    def get_labels(self):
        if not self.labels_path.exists():
            return []

        with self.labels_path.open() as f:
            labels = json.load(f)

        return [LabeledData.from_dict(l) for l in labels]

    def update_labels(self, labels: List[LabeledData]):
        self.save_labels(merge_labels(self.get_labels(), labels))


def merge_labels(a: List[LabeledData], b: List[LabeledData]):
    # Pick last label as more accurate
    merged = {}

    for l in a + b:
        merged[l.ref, l.label_name] = l

    return list(merged.values())
