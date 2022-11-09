import scrapy
import re
from datetime import datetime
from urllib.parse import urljoin
from scrapy_playwright.page import PageMethod


class BunjangSpider(scrapy.Spider):
    name = 'bunjang'

    custom_settings = {
        'FEEDS': {'data/%(name)s_%(time)s.csv': {'format': 'csv', }},
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': '100000'
    }

    def start_requests(self):
        keyword_list = list(map(str, input('Search Keywords : ').split(',')))
        pages = int(input("Max Crawl Pages : "))

        for keyword in keyword_list:
            for page in range(1, pages + 1):
                search_url = f'https://m.bunjang.co.kr/search/products?order=score&page={page}&q={keyword}'
                yield scrapy.Request(
                    url=search_url,
                    callback=self.parse,
                    meta={"playwright": True,
                          "playwright_page_methods": [
                              #PageMethod('evaluate', "window.scrollBy(0, document.body.scrollHeight)"),
                              #PageMethod("wait_for_timeout", 4000),
                              PageMethod("wait_for_selector", '[class^="sc-"]'),
                          ],
                          },
                )

    def parse(self, response):
        products_selector = response.css('[data-pid*="1"]')
        product_regex = re.compile("/products/")

        for product in products_selector:
            product_url = product.css('::attr(href)').get()
            if product_regex.search(product_url):
                yield scrapy.Request(urljoin('https://m.bunjang.co.kr', product_url),
                                     callback=self.parse_product,
                                     meta={"playwright": True})

    def parse_product(self, response):
        product_src = response.css('div.sc-LKuAh.NhTxc > img.sc-iBEsjs.ecWVIk ::attr(src)').get()
        product_title = response.css('div.ProductSummarystyle__Name-sc-oxz0oy-4.gYcooF ::Text').get()
        product_price = response.css('div.ProductSummarystyle__Price-sc-oxz0oy-6.dJuwUw ::Text').get()
        product_seller = response.css('a.ProductSellerstyle__Name-sc-1qnzvgu-7.bPWHcM ::Text').get()

        yield {
            "marketplace": self.name,
            "detected_time": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "product_href": response.request.url,

            "product_src": product_src,
            'product_title': product_title,
            'product_price': product_price,
            'product_seller': product_seller
        }

