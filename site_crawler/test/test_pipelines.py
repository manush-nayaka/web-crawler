import unittest
import sys
from importlib import import_module
from .utils import *

class TestQuotesPipeline(unittest.TestCase):
    def setUp(self):
        sys.path.append("../")
        self.pipeline_module = import_module("site_crawler.pipelines"  , package="pipelines")
        self.spider_module =  import_module("site_crawler.spiders.quotes_spider"  , package="quotes_spider")
        self.spider = self.spider_module.SpiderWeb()
        self.pipelines = list()
        self.pipelines.append(self.pipeline_module.QuotesPipeline())
        self.pipelines.append(self.pipeline_module.UrlLinkPipeline())

    def test_pipeline_methods(self):
        for each in self.pipelines:
            self.assertTrue(check_pipeline_methods(each))

    def test_parse(self):
        self.test_pipeline_methods()

