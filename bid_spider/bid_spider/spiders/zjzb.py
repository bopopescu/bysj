# -*- coding: utf-8 -*-
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
        }
}


class ZjzbSpider(scrapy.Spider):
    name = 'zjzb'
    # allowed_domains = ['zhejiang.bidchance.com/tsp_330000_0_01_0_1.html']
    start_urls = ['http://zhejiang.bidchance.com/tsp_330000_90_01_0_1.html/']

    def parse(self, response):
        get_trs = response.css("#lie tr")
        for tr in get_trs:
            title = tr.xpath("//*/td[2]/a/@title").extract()[0]
            url = tr.xpath("//*/td[2]/a/@href").extract()[0]
            publish_date = tr.xpath("//*/td[4]/text()").extract()[0]
            yield Request(url=url,
                          meta={
                              "title": title,
                              "publish_date": publish_date,
                          },
                          callback=self.parase_detail)

    def parase_detail(self, response):
        item_loader = BidcontentItemLoader(item=BidcontentItem(), response=response)
        item_loader.add_value("title", response.meta.get("title"))
        item_loader.add_value("publish_date", response.meta.get("publish_date"))
        item_loader.add_value("url", response.url)
        item_loader.add_value("industry", " ")
        item_loader.add_value("region", "浙江")
        item_loader.add_value("fund", " ")
        # item_loader.add_css("content", ".ggxx-info")
        item_loader.add_value("content", response.text)
        item_loader.add_value("bid_id", response.text)
        item_loader.add_value("dead_date", response.text)
        bid_items = item_loader.load_item()
        yield bid_items
