import argparse
from scrapy import spiderloader
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner

parser = argparse.ArgumentParser(description='ECS - Comment', formatter_class=argparse.RawTextHelpFormatter, conflict_handler='resolve')


def get_arguments():
    parser.add_argument('-m', '--mode', type=str, choices=['p', 's'], required=True, metavar=("'p' or 's'"),
                        help='Processing Mode (Parallel or Sequentially)')

    parser.add_argument('-t', '--target', type=str, required=True, nargs='+', metavar=("'Market_1' 'Market_2'"),
                        help='Set Marketplaces')

    parser.add_argument('-k', '--keyword', type=str, required=True, nargs='+', metavar=("'Keyword_1' 'Keyword_2'"),
                        help='Set Search Keywords')

    parser.add_argument('-p', '--page', type=int, required=True, nargs='+',
                        metavar=("'Market_1_pages' 'Market_2_pages'"), help='Set Crawl Pages for each Marketplace')

    parser.add_argument('-x', '--proxy', type=str, choices=['y', 'n'], default='n', metavar=("'y' or 'n'"),
                        help='Enable Proxy')

    parser.add_argument('-i', '--include', type=str, nargs='+', metavar=("'IncludeKeyword_1' 'IncludeKeyword_2'"),
                        help='Set Include Keywords')

    parser.add_argument('-e', '--exclude', type=str, nargs='+', metavar=("'ExcludeKeyword_1' 'ExcludeKeyword_2'"),
                        help='Set Exclude Keywords')

    parser.add_argument('-a', '--auth', type=str, nargs='+', metavar=("'AuthSeller_1' 'AuthSeller_2'"),
                        help='Set Authorised Sellers')

    parser.add_argument('-u', '--unth', type=str, nargs='+', metavar=("'UnauthSeller_1' 'UnauthSeller_2'"),
                        help='Set Unauthorised Sellers')

    #parser.add_argument('-s', '--schedule', type=str, choices=['y', 'n'], default='n', metavar=("'y' or 'n'"), help='Set Schedule')

    _args = parser.parse_args()

    return _args


def ecs_main():
    args = get_arguments()

    if args.mode == 'p':
        parallel_mode(args.target, args.keyword)
    sequentially_mode(args.target, args.keyword)


def parallel_mode(p_targets, p_keyword):
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    print(f"Detection Targets : {p_targets}")
    print(f"Keywords : {p_keyword}")

    for target in p_targets:
        print(f"Spider '{target}' launched!")
        process.crawl(target)

    process.start()


def sequentially_mode(s_targets, s_keyword):
    settings = get_project_settings()
    configure_logging(settings)
    runner = CrawlerRunner(settings)

    print(f"Detection Targets : {s_targets}")
    print(f"Keywords : {s_keyword}")

    @defer.inlineCallbacks
    def crawl():
        for target in s_targets:
            print(f"Spider '{target}' launched!")
            yield runner.crawl(target)
        reactor.stop()

    crawl()
    reactor.run()


if __name__ == '__main__':
    #print(spider_loader.list())
    ecs_main()
