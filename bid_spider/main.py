# 调试文件
from scrapy.cmdline import execute
import os
import sys
from tools import crawl_xici_ip
fpath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(fpath)
crawl_xici_ip.crawl_ips()
# execute(["scrapy", "crawl", "getbid"])
# execute(["scrapy", "crawl", "jszb"])
# execute(["scrapy", "crawl", "bjzb"])
# execute(["scrapy", "crawl", "shzb"])
# execute(["scrapy", "crawl", "zjzb"])
# execute(["scrapy", "crawl", "bdczb"])
