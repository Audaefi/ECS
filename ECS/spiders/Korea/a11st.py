import scrapy
from datetime import datetime
from scrapy_playwright.page import PageMethod


class A11stSpider(scrapy.Spider):
    name = '11st'

    custom_settings = {
        'FEEDS': {'data/%(name)s_%(time)s.csv': {'format': 'csv', }},
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': '100000'
    }

    def start_requests(self):
        keyword_list = list(map(str, input('Search Keywords : ').split(',')))
        pages = int(input("Max Crawl Pages : "))

        for keyword in keyword_list:
            for page in range(1, pages + 1):
                search_url = f'https://search.11st.co.kr/Search.tmall?kwd={keyword}#viewType%%L%%list%%3$$sortCd%%N%%%EC%B5%9C%EC%8B%A0%EC%88%9C5$$pageNum%%{page}%%'
                yield scrapy.Request(
                    url=search_url,
                    callback=self.parse,
                    meta={"playwright": True,
                          "playwright_page_methods": [
                              PageMethod('evaluate', "window.scrollBy(0, document.body.scrollHeight)"),
                              PageMethod("wait_for_selector", '[class="c_card c_card_list"]'),
                          ],
                          },
                )

    def parse(self, response):
        products_selector = response.css('[class="c_card c_card_list"]')

        for product in products_selector:
            product_url = product.css('div.c_prd_thumb > a ::attr(href)').get()
            yield scrapy.Request(product_url,
                                 callback=self.parse_product,
                                 meta={"playwright": False,
                                      "playwright_page_methods": [
                                          PageMethod(
                                              "wait_for_selector",
                                              '[class="box__viewer-container"]'),
                                      ],
                                      })

    def parse_product(self, response):
        product_src = response.css('div.img_full > img ::attr(src)').get()
        product_title = response.xpath('.//title/text()').get()
        product_price = response.css('span.value ::Text').get()
        product_seller = response.css('h1.c_product_store_title > a ::Text').get().strip()

        yield {
            "marketplace": self.name,
            "detected_time": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "product_href": response.request.url,

            "product_src": product_src,
            'product_title': product_title.strip(),
            'product_price': product_price,
            'product_seller': product_seller
        }

