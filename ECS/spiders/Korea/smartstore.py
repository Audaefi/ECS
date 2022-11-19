# C
import scrapy
from datetime import datetime
from scrapy_playwright.page import PageMethod
from ECS.items import EcsItem
from ECS.main import get_arguments


class SmartstoreSpider(scrapy.Spider):
    name = 'smartstore'

    custom_settings = {
        'FEEDS': {'data/%(name)s_%(time)s.csv': {'format': 'csv', }},
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': '100000'
    }

    def start_requests(self):
        args = get_arguments()
        query_data = {marketplace: page for marketplace, page in zip(args.target, args.page)}

        for keyword in args.keyword:
            for page in range(1, query_data['smartstore'] + 1):
                search_url = f"https://search.shopping.naver.com/search/all?exrental=true&exused=true&frm=NVSHCHK&npayType=2&origQuery={keyword}&pagingIndex={page}&pagingSize=40&productSet=checkout&query={keyword}&sort=date&timestamp=&viewType=list"
                yield scrapy.Request(search_url, callback=self.parse_page, meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_methods": [
                        PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                        PageMethod("wait_for_timeout", 2000),

                    ],
                    "errback": self.errback,
                    "pd_keyword": keyword,
                })

    async def parse_page(self, response):
        page = response.meta["playwright_page"]
        # await page.screenshot(path="example.png", full_page=True)
        await page.close()
        pd_keyword = response.meta["pd_keyword"]
        products_selector = response.css('[data-testid="SEARCH_PRODUCT"]')

        for product in products_selector:
            product_url = product.css('::attr(href)').get()
            yield scrapy.Request(product_url,
                                 callback=self.parse_product,
                                 meta={"playwright": True, "playwright_include_page": True, "playwright_page_methods": [
                                     PageMethod("wait_for_timeout", 2000)
                                 ], "product_url": product_url, "pd_keyword": pd_keyword})

    async def parse_product(self, response):
        page = response.meta["playwright_page"]
        await page.close()
        #smartstore_regex = re.compile("smartstore.naver.com")

        if response.css('[class="_23RpOU6xpc _2KRGoy-HE2"]'):
            product_src = response.css('[class="_23RpOU6xpc _2KRGoy-HE2"] > img ::attr(src)').get()
        elif response.css('[class="_23RpOU6xpc"]'):
            product_src = response.css('[class="_23RpOU6xpc"] > img ::attr(src)').get()

        #if smartstore_regex.search(response.request.url):

        product_data = EcsItem()
        product_data['detected_time'] = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        product_data['marketplace'] = self.name
        product_data['search_keyword'] = response.meta["pd_keyword"]
        product_data['product_href'] = response.meta["product_url"]
        product_data['product_src'] = product_src
        product_data['product_title'] = response.css('[class="_3oDjSvLwq9 _copyable"] ::Text').get()
        product_data['product_price'] = response.css('[class="_1LY7DqCnwR"] ::Text').get()
        product_data['product_seller'] = response.css('[class="_1gAVrxQEks"] ::Text').get()

        yield product_data

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
