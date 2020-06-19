import hashlib
import json
from dataclasses import asdict, dataclass, replace
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from .types import Candidate, LabeledData

# Alisases for types
UrlType = str
VersionType = int


@dataclass(frozen=True)
class PageInfo:
    # The relative path where the particular item is stored
    path: str
    timestamp: str
    url: UrlType
    version: VersionType


def _hash(txt: str):
    m = hashlib.sha256()
    m.update(txt.encode())
    return m.hexdigest()


class StoreIndex:
    def __init__(self, data: Dict[UrlType, Dict[VersionType, PageInfo]]):
        """A simple index to retrieve information about the store"""
        self._data = data

    @classmethod
    def from_dict(cls, data: Dict[Any, Any]):
        return cls(
            {
                url: {int(v): PageInfo(**pi) for v, pi in versions.items()}
                for url, versions in data.items()
            }
        )

    def to_dict(self):
        return {
            url: {v: asdict(pi) for v, pi in versions.items()}
            for url, versions in self._data.items()
        }

    def has_page(self, url: UrlType) -> bool:
        return url in self._data

    def get_page_info(self, url: UrlType, version: VersionType) -> PageInfo:
        return self._data[url][version]

    def get_latest_version(self, url: UrlType) -> int:
        if not self.has_page(url):
            raise ValueError(f"url {url} not in index")

        if not self._data[url]:
            raise ValueError(f"No versions stored for url {url}")

        return max(self._data[url])

    def set_page_info(self, url: UrlType, page_info: PageInfo) -> None:
        if not self.has_page(url):
            self._data[url] = {}
        self._data[url].update({page_info.version: page_info})

    def get_latest_page_info(self, url: UrlType) -> PageInfo:
        """Get the latest page info"""
        return self.get_page_info(url, self.get_latest_version(url))


IndexType = Dict[UrlType, Dict[VersionType, PageInfo]]


class Store:
    def __init__(self, store_dir):
        self.dir = Path(store_dir)
        if not self.dir.exists():
            self.dir.mkdir()

        self._index_path = self.dir / "index.json"
        self._index = StoreIndex({})

        if self._index_path.exists():
            with self._index_path.open() as f:
                self._index = StoreIndex.from_dict(json.load(f))

    def get_page(self, url: str) -> "Page":
        return Page(self, self._index.get_latest_page_info(url))

    def new_page(self, url: str) -> "Page":
        """Store a new version of a page"""
        if self._index.has_page(url):
            version = self._index.get_latest_version(url) + 1
        else:
            version = 1

        timestamp = datetime.now().isoformat()
        path = self.dir / _hash(url) / f"{version:04d}"
        page_info = PageInfo(
            path=str(path.relative_to(self.dir)),
            version=version,
            url=url,
            timestamp=timestamp,
        )

        if not path.exists():
            path.mkdir(parents=True)

        self._index.set_page_info(url, page_info)
        self._flush_index()
        return Page(self, page_info)

    def _flush_index(self):
        with self._index_path.open("w") as f:
            json.dump(self._index.to_dict(), f)


class Page:
    def __init__(self, store: Store, info: PageInfo):
        self._store = store
        self.info = info
        self._path = store.dir / self.info.path

    @property
    def screenshot_path(self) -> Path:
        return self._path / "screenshot.png"

    @property
    def candidates_path(self) -> Path:
        return self._path / "candidates.json"

    @property
    def labels_path(self) -> Path:
        return self._path / "labels.json"

    @property
    def dom_path(self) -> Path:
        return self._path / "dom.html"

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
