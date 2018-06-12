# -*- coding: utf-8 -*-
# 获取北京的招标信息
import scrapy
from scrapy.http import Request
from ..items import BidcontentItem, BidcontentItemLoader
import re
import requests
custom_settings = {
    'DEFAULT_REQUEST_HEADERS': {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
    }
}


class BjzbSpider(scrapy.Spider):
    name = 'bjzb'
    # allowed_domains = ['bjggzyfw.gov.cn/cmsbj/jyxxggjtbyqs/']
    start_urls = ['https://www.bjggzyfw.gov.cn/cmsbj/jyxxggjtbyqs/index.html']

    def parse(self, response):
        get_lis = response.css(".article-list2 li")
        for li in get_lis:
            title = li.css("::attr(title)").extract()[0]
            url = li.css("::attr(href)").extract()[0]
            url = "https://www.bjggzyfw.gov.cn"+str(url)
            yield Request(url=url,
                          meta={
                              "title": title,
                          },
                          callback=self.parase_detail)

    def parase_detail(self,response):
        item_loader = BidcontentItemLoader(item=BidcontentItem(), response=response)
        item_loader.add_value("title", response.meta.get("title"))
        item_loader.add_css("publish_date", ".div-title2")
        item_loader.add_value("url", response.url)
        item_loader.add_value("industry", " ")
        item_loader.add_value("region", "北京")
        item_loader.add_value("fund", " ")
        item_loader.add_value("content", response.text)
        item_loader.add_value("bid_id", response.text)
        item_loader.add_value("dead_date", response.text)
        bid_items = item_loader.load_item()
        yield bid_items

    def start_requests(self):
        start_url = "https://www.bjggzyfw.gov.cn/cmsbj/jyxxggjtbyqs/"
        pages = []
        url = "https://www.bjggzyfw.gov.cn/cmsbj/jyxxggjtbyqs/index.html"
        # response = requests.get(url)
        # nums = response.css(".pages-list li a::text").extract()[0]
        # nums = re.match(".*/(\d*)", nums, re.DOTALL).group(1)
        page = Request(url)
        pages.append(page)
        for i in range(2, 507):
            url = start_url+"index_"+str(i)+".html"
            page = Request(url)
            pages.append(page)
        return pages