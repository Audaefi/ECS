import scrapy


class WalmartSpider(scrapy.Spider):
    name = 'walmart'
    allowed_domains = ['www.walmart.com']
    start_urls = ['http://www.walmart.com/']

    def parse(self, response):
        pass
