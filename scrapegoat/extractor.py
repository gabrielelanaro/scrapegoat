from selenium import webdriver

from .types import Candidate


class PageExtractor:

    """Extract box candidates from web pages"""

    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver

    @classmethod
    def default(cls):
        options = webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome("./chromedriver", options=options)
        return cls(driver)

    def get(self, url: str) -> Candidate:
        # Load the url
        self.driver.get(url)
        S = lambda X: self.driver.execute_script(
            "return document.body.parentNode.scroll" + X
        )
        self.driver.set_window_size(
            S("Width"), S("Height")
        )  # May need manual adjustment

        # Retrieve all the boxes and element
        JSCODE = open("immoscout/js/retrieve.js").read()
        candidates = self.driver.execute_script(JSCODE + "return main();")
        for c in candidates:
            c.update(url=url)

        return [Candidate.from_dict(c) for c in candidates]

    def save_screenshot(self, path: str = "/tmp/screenshot.png") -> None:
        self.driver.find_element_by_tag_name("html").screenshot(path)
