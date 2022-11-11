import scrapy
import re
from urllib.parse import urljoin
from datetime import datetime
from scrapy_playwright.page import PageMethod


class ShopeeIdSpider(scrapy.Spider):
    name = 'shopee_id'

    custom_settings = {
        'FEEDS': {'data/%(name)s_%(time)s.csv': {'format': 'csv', }},
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': '100000'
    }

    def start_requests(self):
        keyword_list = list(map(str, input('Search Keywords : ').split(',')))
        pages = int(input("Max Crawl Pages : "))

        for keyword in keyword_list:
            for page in range(1, pages + 1):
                search_url = f"https://shopee.co.id/search?keyword={keyword}&page={page}"
                yield scrapy.Request(
                    url=search_url,
                    callback=self.parse,
                    meta={"playwright": True,
                          "playwright_page_methods": [
                              PageMethod('evaluate', "window.scrollBy(0, document.body.scrollHeight)"),
                              PageMethod("wait_for_selector", '[data-sqe="item"]'),
                          ],
                          },
                )

    def parse(self, response):
        products_selector = response.css('[data-sqe="item"]')

        for product in products_selector:
            relative_url = product.css('a ::attr(href)').get()
            product_url = urljoin('https://shopee.co.id', relative_url)
            yield scrapy.Request(product_url,
                                 callback=self.parse_product,
                                 meta={"playwright": True, "playwright_page_methods": [
                                     #PageMethod("wait_for_selector", '_3CXjs-._3DKwBj'),
                                     PageMethod("wait_for_timeout", 2000)
                                     #PageMethod("wait_for_selector", 'div._2rQP1z'),
                                     #PageMethod("wait_for_selector", 'div._2Shl1j'),
                                     #PageMethod("wait_for_selector", 'div._3LoNDM')
                                 ],
                                       })

    def parse_product(self, response):
        product_src = response.css('div._3iW6K2').get()
        product_title = response.css('div._2rQP1z > span ::Text').get()
        product_price = response.css('div._2Shl1j ::Text').get()
        product_seller = response.css('div._3LoNDM ::Text').get()

        yield {
            "marketplace": self.name,
            "detected_time": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "product_href": response.request.url,

            "product_src": product_src, #re.findall('\(([^)]+)', product_src)
            'product_title': product_title,
            'product_price': product_price,
            'product_seller': product_seller
        }
