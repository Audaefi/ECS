import scrapy
from datetime import datetime
from scrapy_playwright.page import PageMethod


class GmarketSpider(scrapy.Spider):
    name = 'gmarket'

    custom_settings = {
        'FEEDS': {'data/%(name)s_%(time)s.csv': {'format': 'csv', }},
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': '100000'
    }

    def start_requests(self):
        keyword_list = list(map(str, input('Search Keywords : ').split(',')))
        pages = int(input("Max Crawl Pages : "))

        for keyword in keyword_list:
            for page in range(1, pages + 1):
                search_url = f'https://browse.gmarket.co.kr/search?keyword={keyword}&s=3&k=0&p={page}'

                yield scrapy.Request(
                    url=search_url,
                    callback=self.parse,
                    meta={"playwright": True,
                          "playwright_page_methods": [
                              #PageMethod('evaluate', "window.scrollBy(0, document.body.scrollHeight)"),
                              PageMethod("wait_for_selector", '[class="box__component box__component-itemcard box__component-itemcard--general"]'),
                          ],
                          },
                )

    def parse(self, response):
        products_selector = response.css('[class="box__component box__component-itemcard box__component-itemcard--general"]')

        for product in products_selector:
            product_url = product.css('a.link__item ::attr(href)').get()
            yield scrapy.Request(product_url,
                                 callback=self.parse_product,
                                 meta={"playwright": False, "playwright_page_methods": [
                                      PageMethod(
                                          "wait_for_selector",
                                          '[class="box__viewer-container"]'),
                                  ],
                                  })

    def parse_product(self, response):
        product_src = response.css('div.box__viewer-container > ul > li.on > a > img ::attr(src)').get()
        product_title = response.css('h1.itemtit ::Text').get().strip()
        product_price = response.css('strong.price_real ::Text').get().strip()
        product_seller = response.css('a.link__seller.sp_vipgroup--before.sp_vipgroup--after ::Text').get()
        #product_seller = response.xpath('.//link__seller.sp_vipgroup--before.sp_vipgroup--after/text()').get()

        yield {
            "marketplace": self.name,
            "detected_time": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "product_href": response.request.url,

            "product_src": product_src,
            'product_title': product_title,
            'product_price': product_price,
            'product_seller': product_seller
        }