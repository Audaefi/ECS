import scrapy
from datetime import datetime
from scrapy_playwright.page import PageMethod


class TmonSpider(scrapy.Spider):
    name = 'tmon'

    custom_settings = {
        'FEEDS': {'data/%(name)s_%(time)s.csv': {'format': 'csv', }},
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': '100000'
    }

    def start_requests(self):
        keyword_list = list(map(str, input('Search Keywords : ').split(',')))
        pages = int(input("Max Crawl Pages : "))

        for keyword in keyword_list:
            for page in range(1, pages + 1):
                search_url = f'http://search.tmon.co.kr/search/?keyword={keyword}&commonFilters=showOptionOnly:true&thr=hs&sortType=BUY_COUNT&page={page}'

                yield scrapy.Request(
                    url=search_url,
                    callback=self.parse,
                    meta={"playwright": True,
                          "playwright_page_methods": [
                              PageMethod('evaluate', "window.scrollBy(0, document.body.scrollHeight)"),
                              PageMethod("wait_for_selector", '[class="anchor"]'),
                          ],
                          },
                )

    def parse(self, response):
        products_selector = response.css('[class="anchor"]')

        for product in products_selector:
            product_url = product.css('::attr(href)').get()
            yield scrapy.Request(product_url,
                                 callback=self.parse_product,
                                 meta={"playwright": False, "playwright_page_methods": [
                                     PageMethod(
                                         "wait_for_selector",
                                         '[class="lst"]'),
                                 ],
                                       })

    def parse_product(self, response):
        product_src = response.css('#image-wrapper > li > img ::attr(src)').get()
        product_title = response.css('div.deal_title > h2 ::Text').get().strip()
        product_price = response.css('div.deal_price > p.deal_price_sell > strong ::Text').get().strip()
        product_seller = ''
        #product_seller = response.css('div.deal_title > p > span ::Text').get().strip()

        yield {
            "marketplace": self.name,
            "detected_time": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "product_href": response.request.url,

            "product_src": product_src,
            'product_title': product_title,
            'product_price': product_price,
            'product_seller': product_seller
        }
