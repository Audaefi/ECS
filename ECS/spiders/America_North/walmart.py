import scrapy
from datetime import datetime
from urllib.parse import urljoin
from scrapy_playwright.page import PageMethod
import ECS.settings


class WalmartSpider(scrapy.Spider):
    name = 'walmart'

    custom_settings = {
        'FEEDS': {'data/%(name)s_%(time)s.csv': {'format': 'csv', }},
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': '100000'
    }

    def start_requests(self):
        keyword_list = list(map(str, input('Search Keywords : ').split(',')))
        pages = int(input("Max Crawl Pages : "))

        for keyword in keyword_list:
            for page in range(1, pages + 1):
                search_url = f"https://www.walmart.com/search?q={keyword}&page={page}&affinityOverride=default"
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

        products_selector = response.css('[class="absolute w-100 h-100 z-1 hide-sibling-opacity"]')

        for product in products_selector:
            relative_url = product.css('::attr(href)').get()
            product_url = urljoin('https://www.walmart.com', relative_url)
            yield scrapy.Request(product_url,
                                 callback=self.parse_product,
                                 meta={"playwright": True,
                                       "playwright_page_methods": [
                                           PageMethod("wait_for_timeout", 2000),
                                       ],
                                       "product_url": product_url
                                       })

    def parse_product(self, response):
        page_url = response.meta["product_url"]
        product_src = response.css('img.noselect.db ::attr(src)').get()
        # re.findall(r"colorImages':.*'initial':\s*(\[.+?\])},\n", response.text)[0]
        product_title = response.css('[itemprop="name"] ::Text').get()
        product_price = response.css('[itemprop="price"] ::text').get("")
        product_seller = response.css('[link-identifier="Generic Name"] ::text').get("")

        yield {
            "marketplace": self.name,
            "detected_time": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "product_href": page_url,
            "product_src": product_src,
            'product_title': product_title,
            'product_price': product_price,
            'product_seller': product_seller
        }

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
