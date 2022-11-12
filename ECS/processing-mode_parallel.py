from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

# KOREA
from ECS.spiders.Korea.a11st import A11stSpider
from ECS.spiders.Korea.auction import AuctionSpider
from ECS.spiders.Korea.bunjang import BunjangSpider
from ECS.spiders.Korea.coupang import CoupangSpider
from ECS.spiders.Korea.gsshop import GsshopSpider
from ECS.spiders.Korea.gmarket import GmarketSpider
from ECS.spiders.Korea.hellomarket import HellomarketSpider
from ECS.spiders.Korea.smartstore import SmartstoreSpider
from ECS.spiders.Korea.ssg import SsgSpider
from ECS.spiders.Korea.tmon import TmonSpider
from ECS.spiders.Korea.wemakeprice import WemakepriceSpider

# SEA
from ECS.spiders.Korea.lazada_my import LazadaSpider
from ECS.spiders.Korea.lazada_ph import LazadaPhSpider
from ECS.spiders.Korea.lazada_th import LazadaThSpider
from ECS.spiders.Korea.lazada_vn import LazadaVnSpider


def main():
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    process.crawl(SmartstoreSpider)
    process.crawl(GmarketSpider)
    process.start()  # the script will block here until the crawling is finished


if __name__ == '__main__':
    main()
