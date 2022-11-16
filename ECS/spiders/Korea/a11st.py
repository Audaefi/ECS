# C
import scrapy
from datetime import datetime
from scrapy_playwright.page import PageMethod


class A11stSpider(scrapy.Spider):
    name = '11st'

    custom_settings = {
        'FEEDS': {'data/%(name)s_%(time)s.csv': {'format': 'csv', }},
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': '100000'
    }

    def start_requests(self):
        keyword_list = list(map(str, input('Search Keywords : ').split(',')))
        pages = int(input("Max Crawl Pages : "))

        for keyword in keyword_list:
            for page in range(1, pages + 1):
                search_url = f'https://search.11st.co.kr/Search.tmall?kwd={keyword}#pageNum%%{page}%%page%%10$$viewType%%I%%gallery%%13$$sortCd%%SPS%%11%EB%B2%88%EA%B0%80%20%EC%9D%B8%EA%B8%B0%EC%88%9C%%9'
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

    def parse_page(self, response):
        products_selector = response.css('[data-log-actionid-label="product"]')

        for product in products_selector:
            product_url = product.css('::attr(href)').get()
            yield scrapy.Request(product_url,
                                 callback=self.parse_product,
                                 meta={"playwright": False,
                                       "playwright_page_methods": [
                                           PageMethod("wait_for_timeout", 2000),
                                       ],
                                       "product_url": product_url
                                       })

    def parse_product(self, response):
        page_url = response.meta["product_url"]
        product_src = response.css('div.img_full > img ::attr(src)').get()
        product_title = response.xpath('.//title/text()').get()
        product_price = response.css('span.value ::Text').get()
        product_seller = response.css('h1.c_product_store_title > a ::Text').get().strip()

        yield {
            "marketplace": self.name,
            "detected_time": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "product_href": page_url,

            "product_src": product_src,
            'product_title': product_title.strip(),
            'product_price': product_price,
            'product_seller': product_seller
        }

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
