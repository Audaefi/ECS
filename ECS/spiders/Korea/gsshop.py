import scrapy
from datetime import datetime
from scrapy_playwright.page import PageMethod

pageList = ['eyJwYWdlTnVtYmVyIjoxLCJzZWxlY3RlZCI6Im9wdC1wYWdlIn0%3D',
            'eyJwYWdlTnVtYmVyIjoyLCJzZWxlY3RlZCI6Im9wdC1wYWdlIn0%3D',
            'eyJwYWdlTnVtYmVyIjozLCJzZWxlY3RlZCI6Im9wdC1wYWdlIn0%3D',
            'eyJwYWdlTnVtYmVyIjo0LCJzZWxlY3RlZCI6Im9wdC1wYWdlIn0%3D',
            'eyJwYWdlTnVtYmVyIjo1LCJzZWxlY3RlZCI6Im9wdC1wYWdlIn0%3D',
            'eyJwYWdlTnVtYmVyIjo2LCJzZWxlY3RlZCI6Im9wdC1wYWdlIn0%3D',
            'eyJwYWdlTnVtYmVyIjo3LCJzZWxlY3RlZCI6Im9wdC1wYWdlIn0%3D',
            'eyJwYWdlTnVtYmVyIjo4LCJzZWxlY3RlZCI6Im9wdC1wYWdlIn0%3D',
            'eyJwYWdlTnVtYmVyIjo5LCJzZWxlY3RlZCI6Im9wdC1wYWdlIn0%3D',
            'eyJwYWdlTnVtYmVyIjoxMCwic2VsZWN0ZWQiOiJvcHQtcGFnZSJ9',
            'eyJwYWdlTnVtYmVyIjoxMSwic2VsZWN0ZWQiOiJvcHQtcGFnZSJ9',
            'eyJwYWdlTnVtYmVyIjoxMiwic2VsZWN0ZWQiOiJvcHQtcGFnZSJ9',
            'eyJwYWdlTnVtYmVyIjoxMywic2VsZWN0ZWQiOiJvcHQtcGFnZSJ9',
            'eyJwYWdlTnVtYmVyIjoxNCwic2VsZWN0ZWQiOiJvcHQtcGFnZSJ9',
            'eyJwYWdlTnVtYmVyIjoxNSwic2VsZWN0ZWQiOiJvcHQtcGFnZSJ9',
            'eyJwYWdlTnVtYmVyIjoxNiwic2VsZWN0ZWQiOiJvcHQtcGFnZSJ9',
            'eyJwYWdlTnVtYmVyIjoxNywic2VsZWN0ZWQiOiJvcHQtcGFnZSJ9',
            'eyJwYWdlTnVtYmVyIjoxOCwic2VsZWN0ZWQiOiJvcHQtcGFnZSJ9',
            'eyJwYWdlTnVtYmVyIjoxOSwic2VsZWN0ZWQiOiJvcHQtcGFnZSJ9',
            'eyJwYWdlTnVtYmVyIjoyMCwic2VsZWN0ZWQiOiJvcHQtcGFnZSJ9']


class GsshopSpider(scrapy.Spider):
    name = 'gsshop'

    custom_settings = {
        'FEEDS': {'data/%(name)s_%(time)s.csv': {'format': 'csv', }},
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': '100000'
    }

    def start_requests(self):
        keyword_list = list(map(str, input('Search Keywords : ').split(',')))
        pages = int(input("Max Crawl Pages : "))

        for keyword in keyword_list:
            for page in range(0, pages):
                search_url = f'https://with.gsshop.com/shop/search/main.gs?tq={keyword}&rq=&cls=&eh={pageList[page]}'
                yield scrapy.Request(
                    url=search_url,
                    callback=self.parse,
                    meta={"playwright": True,
                          "playwright_page_methods": [
                              PageMethod('evaluate', "window.scrollBy(0, document.body.scrollHeight)"),
                              PageMethod("wait_for_selector", '[class="prd-item"]'),
                          ],
                          },
                )

    def parse(self, response):
        products_selector = response.css('[class="prd-item"]')

        for product in products_selector:
            product_url = product.css('a.prd-item ::attr(href)').get()
            yield scrapy.Request(product_url,
                                 callback=self.parse_product,
                                 meta={"playwright": False, "playwright_page_methods": [
                                     PageMethod("wait_for_selector", '[class="btn_img"]'),
                                     PageMethod("click", selector="a.tab on")
                                 ],
                                       })

    def parse_product(self, response):
        product_src = response.css('a.btn_img ::attr(src)').get()
        product_title = response.css('p.product-title ::Text').get()
        product_price = response.css('span.price-definition-ins > ins > strong ::Text').get()
        product_seller = response.css('p.product-brand-more.jpb-shop-link > a > em ::Text').get()
        # product_seller = response.xpath('.//link__seller.sp_vipgroup--before.sp_vipgroup--after/text()').get()

        yield {
            "marketplace": self.name,
            "detected_time": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "product_href": response.request.url,

            "product_src": product_src,
            'product_title': product_title,
            'product_price': product_price,
            'product_seller': product_seller
        }
