# C
import scrapy
import re
from datetime import datetime
from urllib.parse import urljoin
from scrapy_playwright.page import PageMethod

from ECS.items import EcsItem
from ECS.main import get_arguments


class BunjangSpider(scrapy.Spider):
    name = 'bunjang'

    custom_settings = {
        'FEEDS': {'data/%(name)s_%(time)s.csv': {'format': 'csv', }},
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': '100000'
    }

    def start_requests(self):
        args = get_arguments()
        req_pages = {marketplace: page for marketplace, page in zip(args.target, args.page)}

        for keyword in args.keyword:
            for page in range(1, req_pages[self.name] + 1):
                search_url = f'https://m.bunjang.co.kr/search/products?order=score&page={page}&q={keyword}'
                yield scrapy.Request(search_url, callback=self.parse_page, meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_methods": [
                        PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                        PageMethod("evaluate", "window.scrollBy(document.body.scrollHeight, 0)"),
                        PageMethod("wait_for_timeout", 2000),
                    ],
                    "errback": self.errback,
                    "search_keyword": keyword,
                })

    async def parse_page(self, response):
        page = response.meta["playwright_page"]
        # await page.screenshot(path="example.png", full_page=True)
        await page.close()

        search_keyword = response.meta["search_keyword"]
        products_selector = response.css('[data-pid*="1"]')
        product_regex = re.compile("/products/")

        for product in products_selector:
            relative_url = product.css('::attr(href)').get()
            if product_regex.search(relative_url):
                product_url = urljoin('https://m.bunjang.co.kr', relative_url)
                yield scrapy.Request(product_url,
                                     callback=self.parse_product,
                                     meta={"playwright": True, "playwright_include_page": True,
                                           "playwright_page_methods": [
                                               PageMethod("wait_for_timeout", 2000)
                                           ], "product_href": product_url, "search_keyword": search_keyword})

    async def parse_product(self, response):
        page = response.meta["playwright_page"]
        #await page.screenshot(path="%example.png", full_page=True)
        await page.close()

        product_data = EcsItem()
        product_data['detected_time'] = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        product_data['marketplace'] = self.name
        product_data['search_keyword'] = response.meta["search_keyword"]
        product_data['product_href'] = response.meta["product_href"]
        product_data['product_src'] = response.css('[class="Productsstyle__ProductImageWrapper-sc-13cvfvh-11 fuesQh"] > div > div > img ::attr(src)').get()
        product_data['product_title'] = response.css('[class="ProductSummarystyle__Name-sc-oxz0oy-4 gYcooF"] ::Text').get()
        product_data['product_price'] = response.css('[class="ProductSummarystyle__Price-sc-oxz0oy-6 dJuwUw"] ::Text').get()
        product_data['product_seller'] = response.css('[class="ProductSellerstyle__Name-sc-1qnzvgu-7 bPWHcM"] ::Text').get()
        yield product_data

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
