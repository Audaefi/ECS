# C
import scrapy
from datetime import datetime
from scrapy_playwright.page import PageMethod
from urllib.parse import urljoin

from ECS.items import EcsItem
from ECS.main import get_arguments


class SsgSpider(scrapy.Spider):
    name = 'ssg'

    custom_settings = {
        'FEEDS': {'data/%(name)s_%(time)s.csv': {'format': 'csv', }},
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': '100000'
    }

    def start_requests(self):
        args = get_arguments()
        req_pages = {marketplace: page for marketplace, page in zip(args.target, args.page)}

        for keyword in args.keyword:
            for page in range(1, req_pages[self.name] + 1):
                search_url = f'https://www.ssg.com/search.ssg?target=all&query={keyword}&count=40&page={page}'
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
        products_selector = response.css('[data-unittype="item"]')

        for product in products_selector:
            relative_url = product.css('a ::attr(href)').get()
            product_url = urljoin('https://www.ssg.com', relative_url)  # .split("?")[0]
            yield scrapy.Request(product_url,
                                 callback=self.parse_product,
                                 meta={"playwright": True, "playwright_include_page": True, "playwright_page_methods": [
                                     PageMethod("wait_for_timeout", 2000)
                                 ], "product_href": product_url, "search_keyword": search_keyword})

    async def parse_product(self, response):
        page = response.meta["playwright_page"]
        # await page.screenshot(path="%example.png", full_page=True)
        await page.close()

        product_seller = response.css('[class="cdtl_store_tittx"] ::Text').get()
        if not product_seller: product_seller = response.css('[class="sm"] > span ::Text').get()

        product_data = EcsItem()
        product_data['detected_time'] = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        product_data['marketplace'] = self.name
        product_data['search_keyword'] = response.meta["search_keyword"]
        product_data['product_href'] = response.meta["product_href"]
        product_data['product_src'] = response.css('[id="mainImg"] ::attr(src)').get()
        product_data['product_title'] = response.css('[class="cdtl_info_tit"] ::Text').get().strip()
        product_data['product_price'] = response.css('[class="ssg_price"] ::Text').get()
        product_data['product_seller'] = product_seller
        yield product_data

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
