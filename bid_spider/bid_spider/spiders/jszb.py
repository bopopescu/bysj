# -*- coding: utf-8 -*-
# 获取江苏省的招标信息
import scrapy
import re
import requests
import datetime
from ..items import BidcontentItem, BidcontentItemLoader
from scrapy.http import Request
from urllib import parse
from ..utils.commen import get_md5
from scrapy.loader import ItemLoader# 用来按照不同的规则提取内容的问题，解决了用正则静态的提取问题
from scrapy.http import FormRequest


class JszbSpider(scrapy.Spider):
    name = 'jszb'
    # allowed_domains = ['jstba.org.cn/Home/NewsList.aspx?newstype=1']
    start_urls = ['http://www.jstba.org.cn/Home/NewsList.aspx?newstype=1']

    def parse(self, response):
        # print(response.text)
        # # get_lis = response.xpath("//*[@id='listContent']/div[2]/div[2]/div")
        # # for li in get_lis[1:]:
        # #     page_url = li.css("div a::attr(href)").extract()[0]
        # #     yield Request(url=parse.urljoin(response.url, page_url),
        # #                   callback=self.parse_detail)
        # current_page = int(response.css(".cpb::text").extract()[0])
        # if current_page < 5:
        #     post_url = "http://www.jstba.org.cn/Home/NewsList.aspx?newstype=1"
        #     FP__VIEWSTATE = response.css("#__VIEWSTATE::attr(value)").extract()[0]
        #     FP__VIEWSTATEGENERATOR = response.css("#__VIEWSTATEGENERATOR::attr(value)").extract()[0]
        #     FP__EVENTVALIDATION =response.css("#__EVENTVALIDATION::attr(value)").extract()[0]
        #     post_data = {
        #         '__VIEWSTATE':FP__VIEWSTATE,
        #         '__VIEWSTATEGENERATOR': FP__VIEWSTATEGENERATOR,
        #         '__EVENTTARGET': "AspNetPager1",
        #         '__EVENTARGUMENT': str(current_page+1),
        #         '__EVENTVALIDATION': FP__EVENTVALIDATION,
        #         # 'tempTB': "",
        #         # 'ctl05$tempTB': "",
        #         # 'tbSearchTitle': "",
        #         'AspNetPager1_input': str(current_page)
        #     }
        #     yield FormRequest.from_response(
        #         response,
        #         url=post_url,
        #         formdata=post_data,
        #         headers=header,
        #         callback=self.parse
        #     )

    # def parse_detail(self, response):
        item_loader = BidcontentItemLoader(item=BidcontentItem(), response=response)
        item_loader.add_css("title", "#enBody > div:nth-child(2) > h1")
        item_loader.add_css("publish_date", "#enBody > div:nth-child(2) > div:nth-child(2) > span:nth-child(2)")
        item_loader.add_value("url", response.url)
        item_loader.add_value("industry", " ")
        item_loader.add_value("region", "江苏")
        item_loader.add_value("fund", " ")
        item_loader.add_value("content", response.text)
        item_loader.add_value("bid_id", response.text)
        item_loader.add_value("dead_date", response.text)
        bid_items = item_loader.load_item()
        yield bid_items

    def start_requests(self):
        pages = []
        for i in range(9000, 100005):
            url = "http://www.jstba.org.cn/Home/NewsView.aspx?id="+str(i)
            page = Request(url)
            pages.append(page)
        return pages