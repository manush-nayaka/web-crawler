# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import logging
from site_crawler.items import QuoteItem, UrlLinkItem

class QuotesPipeline(object):
    """pipeline for quotes scrapping"""
    def open_spider(self, spider):
        self.quotes = dict()
        self.path = spider.data_sink + "/quotes/"

    def close_spider(self, spider):
        try:
            if not os.path.exists(self.path):
                os.makedirs(self.path)
            for each_author in self.quotes.keys():
                with open(self.path + each_author.replace(" ","_") + "_quotes.txt", "w") as f:
                    f.write("\n".join(self.quotes[each_author]))
        except OSError as error:
            spider.log("Failed with the OS error %s" %error,logging.ERROR)
        except:
            spider.log("Failed pipeline quotes pipeline",logging.ERROR)

    def process_item(self, item, spider):
        if isinstance(item, QuoteItem):
            try:
                if item["author"] not in self.quotes.keys():
                    self.quotes[item["author"]] = set()
                self.quotes[item["author"]].add(item["quote"])
            except:
                spider.log("Failed to monetize the quote items scrapped",logging.ERROR)
        return item

class UrlLinkPipeline(object):
    """pipeline for url scrapping"""
    def open_spider(self, spider):
        self.urls = dict()
        self.path = spider.data_sink + "/web_links/"
        try:
            if not os.path.exists(self.path):
                os.makedirs(self.path)
            os.remove(self.path+"web_links.txt")
        except OSError:
            pass

    def close_spider(self, spider):
        try:
            if not os.path.exists(self.path):
                os.makedirs(self.path)
            with open(self.path + "web_links.txt", "w") as f:
                for each_url in self.urls.keys():
                    f.write(each_url + "\t" + ",".join(self.urls[each_url]))
                    f.write("\n")
        except OSError:
            spider.log("Failed to create web_links.txt file",logging.ERROR)
        except:
            spider.log("Failed pipeline url link pipeline",logging.ERROR)
    
    def process_item(self, item, spider):
        if isinstance(item, UrlLinkItem):
            try:
                self.urls[item["url"].replace(spider.domain_name,"")] = set(item["links"])
            except:
                spider.log("Failed to monetize the url items scrapped",logging.ERROR)
        return item
        
