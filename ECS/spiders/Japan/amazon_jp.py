import scrapy


class AmazonJpSpider(scrapy.Spider):
    name = 'amazon_jp'
    allowed_domains = ['www.amazon.com']
    start_urls = ['http://www.amazon.com/']

    def parse(self, response):
        pass
