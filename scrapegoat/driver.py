"""Driver program for this project"""

import json
import pathlib
from dataclasses import asdict

from immoscout.extractor import PageExtractor

from .store import Store


class Driver:
    def __init__(self) -> None:
        self.extractor = PageExtractor.default()

    def extract(self, url: str, store: Store):
        candidates = self.extractor.get(url)

        page = store.get_or_create_page(url)

        self.extractor.save_screenshot(str(page.screenshot_path))
        page.save_candidates(candidates)
        return candidates
