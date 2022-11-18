# C
import scrapy
from datetime import datetime
from scrapy_playwright.page import PageMethod


class SmartstoreSpider(scrapy.Spider):
    name = 'smartstore'

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
                search_url = f"https://search.shopping.naver.com/search/all?exrental=true&exused=true&frm=NVSHCHK&npayType=2&origQuery={keyword}&pagingIndex={page}&pagingSize=40&productSet=checkout&query={keyword}&sort=date&timestamp=&viewType=list"
                yield scrapy.Request(search_url, callback=self.parse_page, meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                        PageMethod("wait_for_timeout", 2000),

                    ],
                    errback=self.errback,
                ))

    async def parse_page(self, response):
        page = response.meta["playwright_page"]
        await page.close()

        products_selector = response.css('[data-testid="SEARCH_PRODUCT"]')

        for product in products_selector:
            product_url = product.css('::attr(href)').get()
            yield scrapy.Request(product_url,
                                 callback=self.parse_product,
                                 meta={"playwright": True, "playwright_include_page": True, "playwright_page_methods": [
                                     PageMethod("wait_for_timeout", 2000)
                                 ], "product_url": product_url})

    async def parse_product(self, response):
        page = response.meta["playwright_page"]
        await page.close()
        #smartstore_regex = re.compile("smartstore.naver.com")

        if response.css('[class="_23RpOU6xpc _2KRGoy-HE2"]'):
            product_src = response.css('[class="_23RpOU6xpc _2KRGoy-HE2"] > img ::attr(src)').get()
        elif response.css('[class="_23RpOU6xpc"]'):
            product_src = response.css('[class="_23RpOU6xpc"] > img ::attr(src)').get()

        page_url = response.meta["product_url"]
        product_title = response.css('[class="_3oDjSvLwq9 _copyable"] ::Text').get()
        product_price = response.css('[class="_1LY7DqCnwR"] ::Text').get()
        product_seller = response.css('[class="_1gAVrxQEks"] ::Text').get()

        #if smartstore_regex.search(response.request.url):
        yield {
            "marketplace": self.name,
            "detected_time": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "product_href": page_url,
            "product_src": product_src,
            'product_title': product_title,
            'product_price': product_price,
            'product_seller': product_seller,
        }

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
