"""Driver program for this project"""

import json
import pathlib
from dataclasses import asdict

from .extractor import PageExtractor
from .store import Store


class Driver:
    def __init__(self, store: Store) -> None:
        self.extractor = PageExtractor.default()
        self.store = store

    def extract(self, url: str, store: Store):
        # We get the url
        candidates = self.extractor.get(url)

        # We store the page, using a new version
        page = self.store.new_page(url)

        self.extractor.save_screenshot(str(page.screenshot_path))
        page.save_candidates(candidates)
        return page
