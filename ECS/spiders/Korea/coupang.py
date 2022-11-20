# C
import scrapy
from datetime import datetime
from urllib.parse import urljoin
from scrapy_playwright.page import PageMethod

from ECS.items import EcsItem
from ECS.main import get_arguments


class CoupangSpider(scrapy.Spider):
    name = 'coupang'

    custom_settings = {
        'FEEDS': {'data/%(name)s_%(time)s.csv': {'format': 'csv', }},
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': '100000'
    }

    def start_requests(self):
        args = get_arguments()
        req_pages = {marketplace: page for marketplace, page in zip(args.target, args.page)}

        for keyword in args.keyword:
            for page in range(1, req_pages[self.name] + 1):
                search_url = f"https://www.coupang.com/np/search?q={keyword}&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=latestAsc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=72&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page={page}&rocketAll=false&searchIndexingToken=&backgroundColor="
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
        products_selector = response.css('[class="search-product-link"]')

        for product in products_selector:
            relative_url = product.css('a ::attr(href)').get()
            product_url = urljoin('https://www.coupang.com', relative_url)
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
        product_data['product_src'] = urljoin('https://', response.css('[class="prod-image__detail"] ::attr(src)').get())
        product_data['product_title'] = response.css('[class="prod-buy-header__title"] ::Text').get()
        product_data['product_price'] = response.css('[class="total-price"] > strong ::Text').get()
        product_data['product_seller'] = response.css('[class="prod-sale-vendor-name"] ::Text').get()
        yield product_data

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
