import scrapy
from datetime import datetime
from urllib.parse import urljoin
from scrapy_playwright.page import PageMethod


class HellomarketSpider(scrapy.Spider):
    name = 'hellomarket'

    custom_settings = {
        'FEEDS': {'data/%(name)s_%(time)s.csv': {'format': 'csv', }},
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': '100000'
    }

    def start_requests(self):
        keyword_list = list(map(str, input('Search Keywords : ').split(',')))
        pages = int(input("Max Crawl Pages : "))

        for keyword in keyword_list:
            for page in range(1, pages + 1):
                search_url = f"https://www.hellomarket.com/search?q={keyword}"
                yield scrapy.Request(
                    url=search_url,
                    callback=self.parse,
                    meta={"playwright": True,
                          "playwright_page_methods": [
                              PageMethod('evaluate', "window.scrollBy(0, document.body.scrollHeight)"),
                              PageMethod("wait_for_selector", '[class="item_wrapper_card"]'),
                          ],
                          },
                )

    def parse(self, response):
        products_selector = response.css('[class="item_wrapper_card"]')

        for product in products_selector:
            relative_url = product.css('a.card card_list ::attr(href)').get()
            product_url = urljoin('https://www.hellomarket.com', relative_url)  # .split("?")[0]
            yield scrapy.Request(product_url, callback=self.parse_product, meta={"playwright": True})

    def parse_product(self, response):
        product_src = response.css('img.view.thumbnail_img.mainItemImg" ::attr(src)').get()
        product_title = response.css('span.item_title ::Text').get()
        product_price = response.css('div.item_price.item_price_bottom ::Text').get()
        product_seller = response.css('section.item_user_info.mobile_item_user_info > div.nick > a ::Text').get()

        yield {
            "marketplace": self.name,
            "detected_time": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "product_href": response.request.url,

            "product_src": product_src,
            'product_title': product_title,
            'product_price': product_price,
            'product_seller': product_seller
        }
