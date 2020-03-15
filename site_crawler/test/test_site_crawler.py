import unittest
import sys
from importlib import import_module
from scrapy.http import Request
from test.responses import fake_response_from_file

class TestSiteCrawler(unittest.TestCase):

    def setUp(self):
        sys.path.append("../")
        self.spider_module =  import_module("site_crawler.spiders.quotes_spider"  , package="quotes_spider")
        self.spider = self.spider_module.SpiderWeb()

    def _test_item_results(self, results):
        request_count = 0
        item_count = 0
        for item in results:
            if isinstance(item, Request):
                request_count += 1
            else:
                item_count  += 1
        self.assertEqual(request_count,57)
        self.assertEqual(item_count,1)

    def test_parse(self):
        results = self.spider.parse(fake_response_from_file('html/sample.html'))
        self._test_item_results(results)
