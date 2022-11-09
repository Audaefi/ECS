import scrapy
from datetime import datetime
from urllib.parse import urljoin
from scrapy_playwright.page import PageMethod


class AuctionSpider(scrapy.Spider):
    name = 'auction'

    custom_settings = {
        'FEEDS': {'data/%(name)s_%(time)s.csv': {'format': 'csv', }},
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': '100000'
    }

    def start_requests(self):
        keyword_list = list(map(str, input('Search Keywords : ').split(',')))
        pages = int(input("Max Crawl Pages : "))

        for keyword in keyword_list:
            for page in range(1, pages + 1):
                search_url = f'https://browse.auction.co.kr/search?keyword={keyword}&itemno=&nickname=&frm=hometab&dom=auction&isSuggestion=No&retry=&=&s=3&k=0&p={page}'
                yield scrapy.Request(
                    url=search_url,
                    callback=self.parse,
                    meta={"playwright": True,
                          "playwright_page_methods": [
                              PageMethod('evaluate', "window.scrollBy(0, document.body.scrollHeight)"),
                              PageMethod("wait_for_selector", '[class="component component--item_card type--general"]'),
                          ],
                          },
                )

    def parse(self, response):
        products_selector = response.css('[class="component component--item_card type--general"]')

        for product in products_selector:
            product_url = product.css('a.link--itemcard::attr(href)').get()
            yield scrapy.Request(product_url, callback=self.parse_product, meta={"playwright": False,
                          "playwright_page_methods": [
                              PageMethod("wait_for_selector", '[class="box__viewer-container"]'),
                          ],
                          })

    def parse_product(self, response):
        product_src = urljoin('http://', response.css('div.item-topgallerywrap > div > div > ul > li > a > img ::attr(src)').get())
        product_title = response.css('h1.itemtit ::Text').get()
        product_price = response.css('strong.price_real ::Text').get()
        product_seller = response.css('div.box__official-store > span > a ::Text').get()

        yield {
            "marketplace": self.name,
            "detected_time": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "product_href": response.request.url,

            "product_src": product_src,
            'product_title': product_title,
            'product_price': product_price,
            'product_seller': product_seller
        }
