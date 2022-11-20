# Scrapy settings for ECS project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#
# ---------------------------------------------------------------------------
from ECS.main import get_arguments
args = get_arguments()


BOT_NAME = 'ECS'
SPIDER_MODULES = ['ECS.spiders']
NEWSPIDER_MODULE = 'ECS.spiders'

#PLAYWRIGHT_LAUNCH_OPTIONS = {'headless': False}
FEED_EXPORT_ENCODING = 'utf-8'

DEFAULT_REQUEST_HEADERS = {
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

ROBOTSTXT_OBEY = False
COOKIES_ENABLED = False
AUTOTHROTTLE_ENABLED = True

AUTOTHROTTLE_START_DELAY = 3
AUTOTHROTTLE_MAX_DELAY = 6

SCRAPEOPS_API_KEY = 'e55b354a-4195-41c7-bb2c-d93bf7fb229d'
SCRAPEOPS_PROXY_ENABLED = False

PROXY_VAL = None
INKEY_PIPE_VAL = None
EXKEY_PIPE_VAL = None
AUTH_PIPE_VAL = None
UNTH_PIPE_VAL = None

if args.proxy == 'y':
    SCRAPEOPS_PROXY_ENABLED = True
    PROXY_VAL = 725

if args.include is not None: INKEY_PIPE_VAL = 400
if args.exclude is not None: EXKEY_PIPE_VAL = 300
if args.auth is not None: AUTH_PIPE_VAL = 200
if args.unth is not None: UNTH_PIPE_VAL = 800


'''
FEEDS = {"s3://rdata-storage/%(name)s/%(name)s_%(time)s.csv": {"format": "csv"}}
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
'''

EXTENSIONS = {
    'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500,
}

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': PROXY_VAL,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}

ITEM_PIPELINES = {
    'ECS.pipelines.DuplicatesPipeline': 100,
    'ECS.pipelines.IncludeKeywordPipeline': INKEY_PIPE_VAL,
    'ECS.pipelines.ExcludeKeywordPipeline': EXKEY_PIPE_VAL,
    'ECS.pipelines.AuthorisedSellerPipeline': AUTH_PIPE_VAL,
    'ECS.pipelines.UnauthorisedSellerPipeline': UNTH_PIPE_VAL,
}


TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
REACTOR_THREADPOOL_MAXSIZE = 20
CONCURRENT_REQUESTS_PER_IP = 2
CONCURRENT_REQUESTS = 50
CONCURRENT_REQUESTS_PER_DOMAIN = 30
#AJAXCRAWL_ENABLED = True
#LOG_LEVEL = 'INFO'
