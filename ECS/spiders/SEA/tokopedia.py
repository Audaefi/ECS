import scrapy
from datetime import datetime
from urllib.parse import urljoin
from scrapy_playwright.page import PageMethod


class TokopediaSpider(scrapy.Spider):
    name = 'tokopedia'

    custom_settings = {
        'FEEDS': {'data/%(name)s_%(time)s.csv': {'format': 'csv', }},
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': '100000'
    }

    def start_requests(self):
        keyword_list = list(map(str, input('Search Keywords : ').split(',')))
        pages = int(input("Max Crawl Pages : "))

        for keyword in keyword_list:
            for page in range(1, pages + 1):
                search_url = f"https://www.tokopedia.com/search?page={page}&q={keyword}&st=product"
                yield scrapy.Request(search_url, callback=self.parse_page, meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                        PageMethod("evaluate", "window.scrollBy(document.body.scrollHeight, 0)"),
                        PageMethod("wait_for_timeout", 2000),

                    ],
                    errback=self.errback,
                ))

    async def parse_page(self, response):
        page = response.meta["playwright_page"]
        await page.close()

        products_selector = response.css('[data-testid="master-product-card"]')

        for product in products_selector:
            relative_url = product.css('div.css-1f2quy8 > a ::attr(href)').get()
            product_url = urljoin('https:', relative_url)
            yield scrapy.Request(product_url,
                                 callback=self.parse_product,
                                 meta={"playwright": True,
                                       "playwright_include_page": True,
                                       "playwright_page_methods": [
                                           PageMethod("wait_for_timeout", 2000),
                                           # PageMethod("wait_for_selector", 'div._2rQP1z'),
                                           # PageMethod("wait_for_selector", 'div._2Shl1j'),
                                           # PageMethod("wait_for_selector", 'div._3LoNDM')
                                       ],
                                       })

    async def parse_product(self, response):
        page = response.meta["playwright_page"]
        await page.close()

        product_src = response.css('div.intrinsic.css-1xopdmj > img ::attr(src)').get()
        product_title = response.css('h1.css-1320e6c ::Text').get()
        product_price = response.css('div.css-1m72sg > div ::Text').get()
        product_seller = response.css('div.css-k008qs > a > h2 ::Text').get()

        yield {
            "marketplace": self.name,
            "detected_time": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "product_href": response.request.url,
            "product_src": product_src,
            'product_title': product_title,
            'product_price': product_price.replace("Rp",""),
            'product_seller': product_seller
        }

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()

