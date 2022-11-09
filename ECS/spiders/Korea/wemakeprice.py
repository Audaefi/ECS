import scrapy
from datetime import datetime
from scrapy_playwright.page import PageMethod


class WemakepriceSpider(scrapy.Spider):
    name = 'wemakeprice'

    custom_settings = {
        'FEEDS': {'data/%(name)s_%(time)s.csv': {'format': 'csv', }},
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': '100000'
    }

    def start_requests(self):
        keyword_list = list(map(str, input('Search Keywords : ').split(',')))
        pages = int(input("Max Crawl Pages : "))

        for keyword in keyword_list:
            for page in range(1, pages + 1):
                search_url = f'https://search.wemakeprice.com/search?searchType=DEFAULT&search_cate=top&keyword={keyword}&isRec=1&_service=5&_type=3&sort=sales&isPopularCategory=Y&page={page}'

                yield scrapy.Request(
                    url=search_url,
                    callback=self.parse,
                    meta={"playwright": True,
                          "playwright_page_methods": [
                              PageMethod('evaluate', "window.scrollBy(0, document.body.scrollHeight)"),
                              PageMethod("wait_for_selector", '[class="list_conts_wrap"]'),
                          ],
                          },
                )

    def parse(self, response):
        products_selector = response.css('[class="list_conts_wrap"]')

        for product in products_selector:
            product_url = product.css('::attr(href)').get()
            yield scrapy.Request(product_url,
                                 callback=self.parse_product,
                                 meta={"playwright": True, "playwright_page_methods": [
                                     PageMethod("wait_for_selector", '[class="info_img"]')
                                 ],
                                       })

    def parse_product(self, response):
        product_src = response.css('div.info_img_wrap > div.info_img > img:nth-child(2) ::attr(src)').get()
        product_title = response.css('div.title_box > h3 ::Text').get()
        product_price = response.css('em.num ::Text').get()
        product_seller = response.css('span.store_name > strong ::Text').get()
        # product_seller = response.xpath('.//link__seller.sp_vipgroup--before.sp_vipgroup--after/text()').get()

        yield {
            "marketplace": self.name,
            "detected_time": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "product_href": response.request.url,

            "product_src": product_src,
            'product_title': product_title,
            'product_price': product_price,
            'product_seller': product_seller
        }