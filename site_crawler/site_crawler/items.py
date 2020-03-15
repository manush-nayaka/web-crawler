# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuoteItem(scrapy.Item):
    author = scrapy.Field()
    quote = scrapy.Field()

class UrlLinkItem(scrapy.Item):
    url = scrapy.Field()
    links = scrapy.Field()
