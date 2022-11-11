import scrapy
from datetime import datetime
from urllib.parse import urljoin
from scrapy_playwright.page import PageMethod


class AlibabaSpider(scrapy.Spider):
    name = 'alibaba'

    custom_settings = {
        'FEEDS': {'data/%(name)s_%(time)s.csv': {'format': 'csv', }},
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': '100000'
    }

    def start_requests(self):
        keyword_list = list(map(str, input('Search Keywords : ').split(',')))
        pages = int(input("Max Crawl Pages : "))

        for keyword in keyword_list:
            for page in range(1, pages + 1):
                search_url = f"https://www.alibaba.com/trade/search?spm=a2700.galleryofferlist.0.0.1e32180apXEclx&fsb=y&IndexArea=product_en&keywords={keyword}&tab=all&viewtype=L&&page={page}"
                yield scrapy.Request(
                    url=search_url,
                    callback=self.parse,
                    meta={"playwright": True,
                          "playwright_page_methods": [
                              PageMethod('evaluate', "window.scrollBy(0, document.body.scrollHeight)"),
                              PageMethod("wait_for_selector", '[data-traffic-product="true"]'),
                          ],
                          },
                )

    def parse(self, response):
        products_selector = response.css('[class="list-no-v2-left__img-container"]')

        for product in products_selector:
            relative_url = product.css('a.list-no-v2-left__img-container::attr(href)').get()
            product_url = urljoin('https:', relative_url)  # .split("?")[0]
            yield scrapy.Request(product_url, callback=self.parse_product, meta={"playwright": False})

    def parse_product(self, response):
        product_src = response.css('img.main-img ::attr(src)').get()
        product_title = response.css('div.product-title > h1 ::Text').get()
        product_price = response.css('[data-spm-anchor-id] ::Text').get()
        product_seller = response.css('div.company-item ::Text').get()

        yield {
            "marketplace": self.name,
            "detected_time": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "product_href": response.request.url,

            "product_src": product_src,
            'product_title': product_title,
            'product_price': product_price,
            'product_seller': product_seller
        }

