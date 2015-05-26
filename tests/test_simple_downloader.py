import simple_downloader
import unittest
from urllib.error import HTTPError

class TestSimpleDownloader(unittest.TestCase):

    def test_download(self):
        self.assertGreater(len(simple_downloader.download('http://map.majncraft.cz/tiles/world/t/-1_-1/-3_-2.png', binary=True)), 1000)
        self.assertRaises(HTTPError, simple_downloader.download, 'http://map.majncraft.cz/tiles/world/t/-19_-3/-591_-73.png', binary=True)

        self.assertIn('seznam.cz', simple_downloader.download('http://www.seznam.cz'))
