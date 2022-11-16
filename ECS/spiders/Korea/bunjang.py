# C
import scrapy
import re
from datetime import datetime
from urllib.parse import urljoin
from scrapy_playwright.page import PageMethod


class BunjangSpider(scrapy.Spider):
    name = 'bunjang'

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

    custom_settings = {
        'FEEDS': {'data/%(name)s_%(time)s.csv': {'format': 'csv', }},
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': '100000'
    }

    def start_requests(self):
        keyword_list = list(map(str, input('Search Keywords : ').split(',')))
        pages = int(input("Max Crawl Pages : "))

        for keyword in keyword_list:
            for page in range(1, pages + 1):
                search_url = f'https://m.bunjang.co.kr/search/products?order=score&page={page}&q={keyword}'
                yield scrapy.Request(search_url, callback=self.parse_page, meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                        PageMethod("evaluate", "window.scrollBy(20000, 0)"),
                        PageMethod("wait_for_timeout", 2000),

                    ],
                ))

    async def parse_page(self, response):
        page = response.meta["playwright_page"]
        await page.close()

        products_selector = response.css('[data-pid*="1"]')
        product_regex = re.compile("/products/")

        for product in products_selector:
            relative_url = product.css('::attr(href)').get()
            if product_regex.search(relative_url):
                product_url = urljoin('https://m.bunjang.co.kr', relative_url)
                yield scrapy.Request(product_url,
                                     callback=self.parse_product,
                                     meta={"playwright": True, "playwright_include_page": True, "product_url": product_url})

    async def parse_product(self, response):
        page = response.meta["playwright_page"]
        await page.close()

        page_url = response.meta["product_url"]
        product_src = response.css('div.sc-LKuAh.NhTxc > img.sc-iBEsjs.ecWVIk ::attr(src)').get()
        product_title = response.css('div.ProductSummarystyle__Name-sc-oxz0oy-4.gYcooF ::Text').get()
        product_price = response.css('div.ProductSummarystyle__Price-sc-oxz0oy-6.dJuwUw ::Text').get()
        product_seller = response.css('a.ProductSellerstyle__Name-sc-1qnzvgu-7.bPWHcM ::Text').get()

        yield {
            "marketplace": self.name,
            "detected_time": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "product_href": page_url,

            "product_src": product_src,
            'product_title': product_title,
            'product_price': product_price,
            'product_seller': product_seller
        }

