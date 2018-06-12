# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from bid_spider.items import BidcontentItem, BidcontentItemLoader


class BdczbSpider(scrapy.Spider):
    name = 'bdczb'
    # allowed_domains = ['http://www.bidchance.com/freesearch.do?']
    start_urls = ['http://www.bidchance.com/freesearch.do?/']

    def parse(self, response):
        get_trs = response.css("#datatbody tr")
        # print(get_trs)
        for tr in get_trs[1:]:
            title = tr.xpath("//*/td[2]/a/span/text()").extract()[0]
            url = tr.xpath("//*/td[2]/a/@href").extract()[0]
            province = tr.xpath("//*/td[3]/text()").extract()[1]
            publish_date = tr.xpath("//*/td[4]/text()").extract()[1]
            yield Request(url=url,
                          meta={
                              "title":title,
                              "province":province,
                              "publish_date":publish_date
                          },
                          callback=self.parase_detail
                          )

    def parase_detail(self, response):
        item_loader = BidcontentItemLoader(item=BidcontentItem(), response=response)
        item_loader.add_value("title", response.meta.get("title"))
        item_loader.add_value("publish_date", response.meta.get("publish_date"))
        item_loader.add_value("url", response.url)
        item_loader.add_value("industry", " ")
        item_loader.add_value("region", response.meta.get("province"))
        item_loader.add_value("fund", " ")
        # item_loader.add_css("content", ".ggxx-info")
        item_loader.add_value("content", response.text)
        item_loader.add_value("bid_id", response.text)
        item_loader.add_value("dead_date", response.text)
        bid_items = item_loader.load_item()
        yield bid_items

    def start_requests(self):
        start_st = "http://www.bidchance.com/freesearch.do?&filetype=&channel=gonggao&currentpage="
        start_ed = "&searchtype=sj&queryword=&displayStyle=title&pstate=&field=all&leftday=&province=&bidfile=&project=&heshi=&recommend=&field=all&jing=&starttime=&endtime=&attachment="
        pages = []
        for i in range(1, 86435):
            url = start_st+str(i)+start_ed
            page = Request(url)
            pages.append(page)
        return pages