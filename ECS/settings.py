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

BOT_NAME = 'ECS'

SPIDER_MODULES = ['ECS.spiders']
NEWSPIDER_MODULE = 'ECS.spiders'

#PLAYWRIGHT_LAUNCH_OPTIONS = {'headless': False}

ROBOTSTXT_OBEY = False
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 4
AUTOTHROTTLE_MAX_DELAY = 9

SCRAPEOPS_API_KEY = 'e55b354a-4195-41c7-bb2c-d93bf7fb229d'
#SCRAPEOPS_PROXY_ENABLED = True
#SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT = True

'''
FEEDS = {"s3://rdata-storage/%(name)s/%(name)s_%(time)s.csv": {"format": "csv"}}
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
'''

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    #'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    #'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
    #'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}
'''
FAKEUSERAGENT_PROVIDERS = [
    #'scrapy_fake_useragent.providers.FakeUserAgentProvider',
    'scrapy_fake_useragent.providers.FakerProvider',
    'scrapy_fake_useragent.providers.FixedUserAgentProvider',  # fall back to USER_AGENT value
]

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36'  # fall back
'''
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

CONCURRENT_REQUESTS = 5
#CONCURRENT_REQUESTS_PER_DOMAIN = 10
