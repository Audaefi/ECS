# C , 프록시 사용 시 차단 문제 있음.
import scrapy
from datetime import datetime
from urllib.parse import urljoin
from scrapy_playwright.page import PageMethod

class AmazonSpider(scrapy.Spider):
    name = 'amazon'

    custom_settings = {
        'FEEDS': {'data/%(name)s_%(time)s.csv': {'format': 'csv', }},
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': '100000'
    }

    def start_requests(self):
        keyword_list = list(map(str, input('Search Keywords : ').split(',')))
        pages = int(input("Max Crawl Pages : "))

        for keyword in keyword_list:
            for page in range(1, pages + 1):
                search_url = f"https://www.amazon.com/s?k={keyword}&page={page}"
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

        products_selector = response.css('[class="a-link-normal s-no-outline"]')

        for product in products_selector:
            relative_url = product.css('::attr(href)').get()
            product_url = urljoin('https://www.amazon.com', relative_url)
            yield scrapy.Request(product_url,
                                 callback=self.parse_product,
                                 meta={"playwright": True,
                                       "playwright_include_page": True,
                                       "playwright_page_methods": [
                                           #PageMethod("wait_for_timeout", 2000),
                                           PageMethod("wait_for_selector", '[class="imgTagWrapper"]'),
                                       ],
                                       "product_url": product_url
                                       })

    async def parse_product(self, response):
        page = response.meta["playwright_page"]
        await page.close()

        page_url = response.meta["product_url"]
        product_src = response.css('[class="imgTagWrapper"] ::attr(src)').get()
        #re.findall(r"colorImages':.*'initial':\s*(\[.+?\])},\n", response.text)[0]
        product_title = response.css('[class="a-size-large product-title-word-break"] ::Text').get().strip()
        product_price = response.css('.a-price-whole ::text').get("")
        if not product_price:
            product_price = response.css('.a-price span[aria-hidden="true"] ::text').get("")
        product_seller = None

        yield {
            "marketplace": self.name,
            "detected_time": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "product_href": page_url,
            "product_src": product_src,
            'product_title': product_title,
            'product_price': product_price.replace("$", ""),
            'product_seller': product_seller
        }

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()

