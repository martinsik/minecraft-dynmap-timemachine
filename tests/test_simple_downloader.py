import simple_downloader


def test_download():
    assert 'seznam.cz' in simple_downloader.download('http://www.seznam.cz')