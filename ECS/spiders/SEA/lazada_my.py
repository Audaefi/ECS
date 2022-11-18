import scrapy
from datetime import datetime
from scrapy_playwright.page import PageMethod


class LazadaMySpider(scrapy.Spider):
    name = 'lazada_my'

    custom_settings = {
        'FEEDS': {'data/%(name)s_%(time)s.csv': {'format': 'csv', }},
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': '100000'
    }

    def start_requests(self):
        keyword_list = list(map(str, input('Search Keywords : ').split(',')))
        pages = int(input("Max Crawl Pages : "))

        for keyword in keyword_list:
            for page in range(1, pages+1):
                search_url = f"https://www.lazada.com.my/catalog/?_keyori=ss&from=input&page={page}&q={keyword}"
                yield scrapy.Request(
                    url=search_url,
                    callback=self.parse,
                    meta={"playwright": True,
                          "playwright_page_methods": [
                              PageMethod('evaluate', "window.scrollBy(0, document.body.scrollHeight)"),
                              PageMethod("wait_for_selector", '[data-tracking="product-card"]'),
                            ],
                          },
                )

    def parse(self, response):
        products_selector = response.css('[data-tracking="product-card"]')

        for product in products_selector:
            link = response.urljoin(product.xpath('.//a[text()]/@href').get())
            yield scrapy.Request(link, callback=self.parse_product, meta={"playwright": False, "playwright_page_methods": [
                            PageMethod("wait_for_selector", '.pdp-price.pdp-price_type_normal.pdp-price_color_orange.pdp-price_size_xl'),
                            PageMethod("wait_for_selector", '.pdp-mod-common-image.gallery-preview-panel__image'),
                            ],
                      })

    def parse_product(self, response):
        product_src = response.css('.pdp-mod-common-image.gallery-preview-panel__image ::attr(src)').get()
        product_title = response.css('.pdp-mod-product-badge-title ::Text').get()
        product_price = response.css('.pdp-price.pdp-price_type_normal.pdp-price_color_orange.pdp-price_size_xl ::Text').get()
        product_seller = response.css('.pdp-link.pdp-link_size_l.pdp-link_theme_black.seller-name__detail-name ::Text').get()

        yield {
            "marketplace": self.name,
            "detected_time": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "product_href": response.request.url,

            "product_src": product_src,
            'product_title': product_title,
            'product_price': product_price.replace("RM", ""),
            'product_seller': product_seller
        }

