# -*- coding: utf-8 -*-

# Scrapy settings for bid_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'bid_spider'

SPIDER_MODULES = ['bid_spider.spiders']
NEWSPIDER_MODULE = 'bid_spider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'bid_spider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
     'Accept-Encoding': 'gzip, deflate',
     'Accept-Language': 'zh-CN,zh;q=0.9',
     'Cache-Control': 'max-age=0',
     'Connection': 'keep-alive',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'bid_spider.middlewares.BidSpiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'bid_spider.middlewares.BidSpiderDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'bid_spider.pipelines.BidSpiderPipeline': 300,
   # 'bid_spider.pipelines.JsonWithPipeline': 1,
   'bid_spider.pipelines.MysqlTwistedPipeline': 2,
   'bid_spider.pipelines.ElasticsearchPipeline': 1,
   # 'bid_spider.pipelines.ConverthtmltopdfPipeline': 345
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

#爬取间隔
DOWNLOAD_DELAY = 1
#激活自定义UserAgent和代理IP
DOWNLOADER_MIDDLEWARES = {
   'bid_spider.middlewares.RandomUserAgentMiddlware': 543,
   'scrapy.downloadermiddleware.useragent.UserAgentMiddleware': None,
}

# 数据库配置
MYSQL_HOST = "localhost"
MYSQL_DBNAME = "bid_spider"
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"

# 设置ip代理为随机类型
RANDOM_UA_TYPE = "random"
# 设置数据库的时间格式
SQL_DATETIME_FORMAT = "%Y-%m-%d"
COMMANDS_MODULE = 'bid_spider.commands'
STORE_PDF_PATH = "E:/pywork/bysj/bid_show/static/zbfile/"