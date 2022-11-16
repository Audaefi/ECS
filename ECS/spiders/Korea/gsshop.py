# C
import scrapy
import re
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

    HEADERS = {
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

    def start_requests(self):
        keyword_list = list(map(str, input('Search Keywords : ').split(',')))
        pages = int(input("Max Crawl Pages : "))

        for keyword in keyword_list:
            for page in range(0, pages):
                search_url = f'https://with.gsshop.com/shop/search/main.gs?tq={keyword}&rq=&cls=&eh={pageList[page]}'
                yield scrapy.Request(search_url, callback=self.parse_page, meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                        PageMethod("evaluate", "window.scrollBy(20000, 0)"),
                        PageMethod("wait_for_timeout", 2000),
                    ],
                    errback=self.errback,
                ))

    def parse_page(self, response):
        products_selector = response.css('a.prd-item')

        for product in products_selector:
            product_url = product.css('::attr(href)').get()
            yield scrapy.Request(product_url,
                                 callback=self.parse_product,
                                 meta={"playwright": True, "playwright_include_page": True, "playwright_page_methods": [
                                     PageMethod('evaluate', "window.scrollBy(0, document.body.scrollHeight)"),
                                     PageMethod("wait_for_timeout", 2000)
                                 ], "product_url": product_url})

    async def parse_product(self, response):
        page = response.meta["playwright_page"]
        await page.close()

        page_url = response.meta["product_url"]
        product_src = response.css('a.btn_img ::attr(src)').get()
        product_title = response.css('[class="product-title"] ::Text').getall()
        # response.css('p.product-title > #text ::Text').get()
        product_price = response.css('span.price-definition-ins > ins > strong ::Text').get()
        product_seller = response.css('p.product-brand-more.jpb-shop-link > a > em ::Text').get()
        # product_seller = response.xpath('.//link__seller.sp_vipgroup--before.sp_vipgroup--after/text()').get()

        if not product_src:
            product_src = response.css('div.swiper-slide > img ::attr(src)').get()
            product_title = response.css('[class="prod-name"] ::Text').getall()
            product_price = response.css('span.price > strong ::Text').get()
            product_seller = response.css('i.brand_name ::Text').getall()

        yield {
            "marketplace": self.name,
            "detected_time": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "product_href": page_url,
            "product_src": product_src,
            'product_title': product_title.replace(",", ""),
            'product_price': product_price,
            'product_seller': product_seller
        }

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
