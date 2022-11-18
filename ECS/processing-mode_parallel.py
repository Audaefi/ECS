from scrapy import spiderloader
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess


def main():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    spider_loader = spiderloader.SpiderLoader.from_settings(settings)
    print(spider_loader.list())

    '''
    for target in spider_loader.list():
        print(f"Detection Target : {target}")
        process.crawl(target)
    process.start()
    '''

    for target in marketplace:
        print(f"Detection Target : {target}")
        process.crawl(target)
    process.start()


if __name__ == '__main__':
    marketplace = list(map(str, input('Marketplace : ').split(',')))
    main()
