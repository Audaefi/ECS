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
        keywords = list(map(str, input('Search Keywords : ').split(',')))
        extract_pages = int(input("Max Crawl Pages : "))

        for keyword in keywords:
            for page in range(1, extract_pages + 1):
                search_url = f"https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&tab=&SearchText={keyword}&viewtype=L&&page={page}"
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

        products_selector = response.css('[class="list-no-v2-left__img-container"]')

        for product in products_selector:
            relative_url = product.css('a.list-no-v2-left__img-container::attr(href)').get()
            product_url = urljoin('https:', relative_url)  # .split("?")[0]
            yield scrapy.Request(product_url, callback=self.parse_product, meta={"playwright": False})

    def parse_product(self, response):

        product_src = response.css('img.main-img ::attr(src)').get()
        product_title = response.css('div.product-title > h1 ::Text').get()

        if response.css('span.promotion'): product_price = response.css('span.promotion ::Text').get()
        elif response.css('div.product-price'): product_price = response.css('div.product-price > div > strong ::Text').get()
        elif response.css('div.price-range > span.price'): product_price = response.css('div.price-range > span.price ::Text').get()

        if response.css('div.company-item'): product_seller = response.css('div.company-item ::Text').get()
        if response.css('a.company-name.company-name-lite-vb'): product_seller = response.css('a.company-name.company-name-lite-vb ::Text').get()

        yield {
            "marketplace": self.name,
            "detected_time": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "product_href": response.request.url,
            "product_src": product_src,
            'product_title': product_title,
            'product_price': product_price.replace("$", ""),
            'product_seller': product_seller
        }

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
