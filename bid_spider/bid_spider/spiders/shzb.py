# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ..items import BidcontentItem, BidcontentItemLoader


class ShzbSpider(scrapy.Spider):
    name = 'shzb'
    # allowed_domains = ['shanghai.bidchance.com/tspt_310000_0_02_0_1.html']
    start_urls = ['http://shanghai.bidchance.com/tspt_310000_0_02_0_1.html']

    def parse(self, response):
        get_trs = response.css("#lie tr")
        for tr in get_trs:
            title = tr.css(".big::attr(title)").extract()[0]
            url = tr.css(".big::attr(href)").extract()[0]
            publish_date = response.xpath("//*/td[4]/text()").extract()
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
        item_loader.add_value("region", "上海")
        item_loader.add_value("fund", " ")
        # item_loader.add_css("content", ".ggxx-info")
        item_loader.add_value("content", response.text)
        item_loader.add_value("bid_id", response.text)
        item_loader.add_value("dead_date", response.text)
        bid_items = item_loader.load_item()
        yield bid_items

    def start_requests(self):
        pages = []
        start_url = "http://shanghai.bidchance.com/tsp_310000_0_02_0_"
        for i in range(1,200):
            url = start_url+str(i)+".html"
            page = Request(url)
            pages.append(page)
        return pages
