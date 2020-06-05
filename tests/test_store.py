from scrapegoat.store import Store


def test_store(tmp_path):
    store = Store(tmp_path / "store")
    page = store.new_page("http://www.google.com")
    assert page.info.version == 1
    assert (store.dir / page.info.path).exists()

    page = store.get_page("http://www.google.com")
    assert page.info.version == 1
    assert (store.dir / page.info.path).exists()


def test_store_new_page(tmp_path):
    store = Store(tmp_path / "store")
    store.new_page("http://www.google.com")
    page = store.new_page("http://www.google.com")
    assert page.info.version == 2
    assert (store.dir / page.info.path).exists()
