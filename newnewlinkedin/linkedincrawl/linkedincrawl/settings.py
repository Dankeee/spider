# Scrapy settings for linkedpy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'linkedincrawl'
#LOG_LEVEL = 'INFO'
DOWNLOAD_DELAY = 2 # delay time per request
SPIDER_MODULES = ['linkedincrawl.spiders']
NEWSPIDER_MODULE = 'linkedincrawl.spiders'
CONCURRENT_REQUESTS_PER_DOMAIN = 5
REDIRECT_MAX_TIMES = 10000
COOKIES_ENABLED = False
# CRAWLERA_ENABLED = True
# CRAWLERA_USER = 'c518cad3c95c4ead91e6be586e6bff81'
# CRAWLERA_PASS = 'kk20080504'
PROXY_SPIDERS = ['linkedincrawl.spiders']

DOWNLOADER_MIDDLEWARES = {
    # 'linkedincrawl.middlewares.RandomUserAgent': 1,
    # 'linkedincrawl.middlewares.ProxyMiddleware': 100,
    # 'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 3,
    'linkedincrawl.HttpProxyMiddleware.HttpProxyMiddleware': 4,
    #'scrapy_crawlera.CrawleraMiddleware': 600,
    }

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:9.0.1) Gecko/20100101 Firefox/9.0.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.75 Safari/535.7',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/534.52.7 (KHTML, like Gecko) Version/5.1.2 Safari/534.52.7',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.75 Safari/535.7',
    'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.19 (KHTML, like Gecko) Ubuntu/12.04 Chromium/18.0.1025.151 Chrome/18.0.1025.151 Safari/535.19',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.77 Safari/535.7',
    'Mozilla/5.0 (Windows NT 6.1; rv:9.0.1) Gecko/20100101 Firefox/9.0.1',
    'Mozilla/5.0 (Windows NT 5.1; rv:9.0.1) Gecko/20100101 Firefox/9.0.1',
]
PROXIES = [
    {'ip_port': '123.123.255.213:80', 'user_pass': ''}
  # {'ip_port': '173.220.170.242:7004', 'user_pass': ''},
  # {'ip_port': '107.151.136.212:80', 'user_pass': ''},
  # {'ip_port': '107.151.142.115:80', 'user_pass': ''},
  # {'ip_port': '107.151.152.211:80', 'user_pass': ''},
  # {'ip_port': '210.57.208.14:80', 'user_pass': ''},
  # {'ip_port': '107.151.152.222:80', 'user_pass': ''},
]
