# -*- coding: utf-8 -*-
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
from time import sleep
# 别设置代理，如果设置了，反而会防止爬取

custom_settings = {
    'DEFAULT_REQUEST_HEADERS': {
        # "HOST": "http://www.chinabidding.com",
        # "Referer": "http://www.chinabidding.com/search/proj.htm",
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
    }
}


class GetbidSpider(scrapy.Spider):
    name = 'getbid'
    # allowed_domains = ['http://www.chinabidding.com/search/proj.htm']
    start_urls = ['http://www.chinabidding.com/search/proj.htm']

    def parse(self, response):
        # 进行当前页面的所有url的分析
        get_lis = response.css(".as-pager-body li")
        for li in get_lis:
            next_url = li.css("a::attr(href)").extract()[0]
            title = li.css(".txt::attr(title)").extract()[0]
            industry = li.xpath("//*[@class='horizontal']/dd/span[1]/strong/text()").extract()
            region = li.xpath("//*[@class='horizontal']/dd/span[2]/strong/text()").extract()
            fund = li.xpath("//*[@class='horizontal']/dd/span[3]/strong/text()").extract()
            publish_date = li.css(".time::text").extract()[0]

            yield Request(url=parse.urljoin(response.url, next_url),
                          meta={"industry": industry,
                                "region": region,
                                "fund": fund,
                                "publish_date": publish_date,
                                "title": title
                                },
                          # headers=header,
                          callback=self.parse_detail,
                          )

        # 获取下一个next页面，然后递归的调用该函数（终极可用版）
        next_page = response.css(".next").extract()[0]
        if next_page:
            current_page = response.css(".current::text").extract()[0]
            post_url = "http://www.chinabidding.com/search/proj.htm"
            post_data = {
                "infoClassCodes": "0105",
                "currentPage": str(int(current_page)+1),
                "fullText": "",
                "fundSourceCodes": "",
                "normIndustry": "",
                "poClass": "",
                "pubDate": "",
                "rangeType": "",
                "zoneCode": ""
            }
            yield FormRequest.from_response(
                response,
                url=post_url,
                formdata=post_data,
                # headers=header,
                callback=self.parse
            )

# 分析某个url连接里的内容
    def parse_detail (self, response):
        # 标题：title 时间：p_date 行业：industy 地区： region 资金内容：fund 文本内容：content
        # 通过item_loader来获取（主要是xpth和css来选择会写的很烦，需要写很多的判断函数
        # 用scrapy给我们的套件item_loader
        item_loader = BidcontentItemLoader(item=BidcontentItem(), response=response)
        item_loader.add_value("publish_date", response.meta.get("publish_date"))
        item_loader.add_value("title", response.meta.get("title"))
        item_loader.add_value("url", response.url)
        item_loader.add_value("industry", response.meta.get("industry"))
        item_loader.add_value("region", response.meta.get("region"))
        item_loader.add_value("fund", response.meta.get("fund"))
        item_loader.add_value("content", response.text)
        item_loader.add_value("bid_id", response.text)
        item_loader.add_value("dead_date", response.text)
        bid_items = item_loader.load_item()
        yield bid_items

