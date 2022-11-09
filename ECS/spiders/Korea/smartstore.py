import scrapy
import re
from datetime import datetime
from scrapy_playwright.page import PageMethod


class SmartstoreSpider(scrapy.Spider):
    name = 'smartstore'

    custom_settings = {
        'FEEDS': {'data/%(name)s_%(time)s.csv': {'format': 'csv', }},
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': '100000'
    }

    def start_requests(self):
        keyword_list = list(map(str, input('Search Keywords : ').split(',')))
        pages = int(input("Max Crawl Pages : "))

        for keyword in keyword_list:
            for page in range(1, pages + 1):
                search_url = f"https://search.shopping.naver.com/search/all?exrental=true&exused=true&frm=NVSHCHK&npayType=2&origQuery={keyword}&pagingIndex={page}&pagingSize=40&productSet=checkout&query={keyword}&sort=date&timestamp=&viewType=list"
                yield scrapy.Request(
                    url=search_url,
                    callback=self.parse,
                    meta={"playwright": True,
                          "playwright_page_methods": [
                              PageMethod('evaluate', "window.scrollBy(0, document.body.scrollHeight)"),
                              PageMethod("wait_for_selector", '[data-testid="SEARCH_PRODUCT"]'),
                          ],
                          },
                )

    def parse(self, response):
        products_selector = response.css('[data-testid="SEARCH_PRODUCT"]')

        for product in products_selector:
            product_url = product.css('::attr(href)').get()
            yield scrapy.Request(product_url, callback=self.parse_product, meta={"playwright": False, "playwright_page_methods": [
                              PageMethod("wait_for_selector", 'img._2P2SMyOjl6'),
                          ],
                     })

    def parse_product(self, response):
        product_src = response.css('img._2P2SMyOjl6 ::attr(src)').get()
        product_title = response.css('div._1ziwSSdAv8 > div.CxNYUPvHfB > h3 ::Text').get()
        product_price = response.css('span._1LY7DqCnwR ::Text').get()
        product_seller = response.css('span._1gAVrxQEks ::Text').get()

        smartstore_regex = re.compile("https://smartstore.naver.com/")

        if smartstore_regex.search(response.request.url):
            yield {
                "marketplace": self.name,
                "detected_time": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
                "product_href": response.request.url,

                "product_src": product_src,
                'product_title': product_title,
                'product_price': product_price,
                'product_seller': product_seller,
            }
