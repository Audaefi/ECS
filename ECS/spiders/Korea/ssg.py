import scrapy
from datetime import datetime
from scrapy_playwright.page import PageMethod
from urllib.parse import urljoin


class SsgSpider(scrapy.Spider):
    name = 'ssg'

    custom_settings = {
        'FEEDS': {'data/%(name)s_%(time)s.csv': {'format': 'csv', }},
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': '100000'
    }

    def start_requests(self):
        keyword_list = list(map(str, input('Search Keywords : ').split(',')))
        pages = int(input("Max Crawl Pages : "))

        for keyword in keyword_list:
            for page in range(1, pages + 1):
                search_url = f'https://www.ssg.com/search.ssg?target=all&query={keyword}&count=40&page={page}'

                yield scrapy.Request(
                    url=search_url,
                    callback=self.parse,
                    meta={"playwright": True,
                          "playwright_page_methods": [
                              PageMethod('evaluate', "window.scrollBy(0, document.body.scrollHeight)"),
                              PageMethod("wait_for_selector", '[data-unittype="item"]'),
                          ],
                          },
                )

    def parse(self, response):
        products_selector = response.css('[data-unittype="item"]')

        for product in products_selector:
            relative_url = product.css('a.clickable::attr(href)').get()
            product_url = urljoin('https://www.ssg.com', relative_url)  # .split("?")[0]
            yield scrapy.Request(product_url, callback=self.parse_product, meta={"playwright": False})

    def parse_product(self, response):
        product_src = response.css('img.zoom_thumb ::attr(src)').get()
        product_title = response.css('h2.cdtl_info_tit ::Text').get()
        product_price = response.css('em.ssg_price ::Text').get()
        product_seller = response.css('span.cdtl_store_tittx ::Text').get()

        yield {
            "marketplace": self.name,
            "detected_time": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "product_href": response.request.url,

            "product_src": product_src,
            'product_title': product_title,
            'product_price': product_price,
            'product_seller': product_seller,
        }
