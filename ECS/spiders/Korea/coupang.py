import scrapy
from datetime import datetime
from urllib.parse import urljoin
from scrapy_playwright.page import PageMethod


class CoupangSpider(scrapy.Spider):
    name = 'coupang'

    custom_settings = {
        'FEEDS': {'data/%(name)s_%(time)s.csv': {'format': 'csv', }},
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': '100000'
    }

    def start_requests(self):
        keyword_list = list(map(str, input('Search Keywords : ').split(',')))
        pages = int(input("Max Crawl Pages : "))

        for keyword in keyword_list:
            for page in range(1, pages + 1):
                search_url = f"https://www.coupang.com/np/search?q={keyword}&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=latestAsc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=72&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page={page}&rocketAll=false&searchIndexingToken=&backgroundColor="
                yield scrapy.Request(
                    url=search_url,
                    callback=self.parse,
                    meta={"playwright": True,
                          "playwright_page_methods": [
                              PageMethod('evaluate', "window.scrollBy(0, document.body.scrollHeight)"),
                              PageMethod("wait_for_selector", '[class="search-product-link"]'),
                          ],
                          },
                )

    def parse(self, response):
        products_selector = response.css('[class="search-product-link"]')

        for product in products_selector:
            relative_url = product.css('a.search-product-link::attr(href)').get()
            product_url = urljoin('https://www.coupang.com/', relative_url)  # .split("?")[0]
            yield scrapy.Request(product_url, callback=self.parse_product, meta={"playwright": False})

    def parse_product(self, response):
        product_src = urljoin('https://', response.css('img.prod-image__detail ::attr(src)').get())
        product_title = response.css('h2.prod-buy-header__title ::Text').get()
        product_price = response.css('span.total-price > strong ::Text').get()
        product_seller = response.css('a.prod-sale-vendor-name ::Text').get()

        yield {
            "marketplace": self.name,
            "detected_time": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "product_href": response.request.url,

            "product_src": product_src,
            'product_title': product_title,
            'product_price': product_price,
            'product_seller': product_seller
        }


