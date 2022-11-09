# Scrapy settings for ECS project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ECS'

SPIDER_MODULES = ['ECS.spiders']
NEWSPIDER_MODULE = 'ECS.spiders'

#PLAYWRIGHT_LAUNCH_OPTIONS = {'headless': False}

ROBOTSTXT_OBEY = False
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.8
AUTOTHROTTLE_MAX_DELAY = 2.5
#DOWNLOAD_DELAY = 1

SCRAPEOPS_API_KEY = 'e55b354a-4195-41c7-bb2c-d93bf7fb229d'
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
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    #'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    #'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
}

'''
FAKEUSERAGENT_PROVIDERS = [
    'scrapy_fake_useragent.providers.FakeUserAgentProvider',  # this is the first provider we'll try
    'scrapy_fake_useragent.providers.FakerProvider',  # if FakeUserAgentProvider fails, we'll use faker to generate a user-agent string for us
    'scrapy_fake_useragent.providers.FixedUserAgentProvider',  # fall back to USER_AGENT value
]
'''

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

