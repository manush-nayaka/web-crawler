import scrapy
from scrapy.loader import ItemLoader
from site_crawler.items import QuoteItem, UrlLinkItem

class SpiderWeb(scrapy.Spider):
    name = "spidy"   # name of the crawler
    data_sink = "scraped_data"
    allowed_domains=['quotes.toscrape.com'] # allowed domains filtered using middlewares
    domain_name="http://quotes.toscrape.com" # domain name 

    def start_requests(self):
        """
        Initial seed URL
        returns - generator function to yield seed urls
        """
        urls = [
            'http://quotes.toscrape.com/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        callback function post response reception 
        @param response: http response
        returns - generator function UrlLinkItem and QuoteItem
        """
        url_links = self.get_all_url_links(response)
        if url_links is not None:
            for each_url in url_links:
                yield response.follow(each_url, self.parse)
        u = UrlLinkItem()
        u["url"] = response.url
        u["links"] = url_links
        yield u 
        for quote in response.css('div.quote'):
            q = QuoteItem()
            q["author"] = quote.xpath('span/small/text()').get()
            q["quote"] = quote.css('span.text::text').get()
            yield q

    def get_all_url_links(self, response):
        """
        returns all url links in a response moved to reuse this method in subsequent derived classes
        @param response: http response
        returns - list of urls
        """
        url_links = response.css('a::attr("href")').getall()
        return url_links
