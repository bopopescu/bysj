# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import re
from w3lib.html import remove_tags
from scrapy.loader import ItemLoader
from .settings import SQL_DATETIME_FORMAT
import time, datetime
from .modes.es_type import BidType
from .tools import HTML_Convert_To_pdf
from elasticsearch_dsl import connections
from .settings import STORE_PDF_PATH
es = connections.create_connection(BidType._doc_type.using)


class BidSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# 去除标题里面的空格，制表符等
def get_title(value):
    value = re.split("\t|\n|\r|\s*", value)
    return value


# 获取省份
def get_province(value):
    match_object = "(.*)省"
    ans = re.match(match_object, value, re.DOTALL)
    if ans:
        value = ans.group(1)
    return value


# 获取招标文件的编号
def get_bid_id(content):
    match_obj = ".*编号(:|：)([a-zA-Z0-9-]+)"
    ans = re.match(match_obj, content, re.DOTALL)
    bid_id = " "
    if ans:
        bid_id = str(ans.group(2))
    return bid_id


# 获取发布时间，格式化
def get_publish_time(value):
    value = value.replace("发布时间：", "")
    value = value.replace("发布日期：", "")
    value = value.replace("年", "-")
    value = value.replace("月", "-")
    value = value.replace("日", "")
    ans = re.match(".*(\d{4}-\d+-\d+)", value, re.DOTALL)
    if ans:
        value = ans.group(1)
    return value


# 处理正文内容，去除js,css,注释等，获取得到纯文本
def handle_content(value):
    reCOMM = r'<!--.*?-->'
    reTRIM = r'<{0}.*?>([\s\S]*?)<\/{0}>'
    reTAG = r'<[\s\S]*?>|[ \t\r\f\v]'
    value = re.sub(reCOMM, "", value)
    value = re.sub(reTRIM.format("script"), "", re.sub(reTRIM.format("style"), "", value))
    value = re.sub(reTAG, "", value)
    value = value.replace("&nbsp", "")
    value = value.replace(";", "")
    addr_list = re.split("\t|\n|\r", value)
    return "".join(addr_list)


# 获取截止时间
def getdeadline(value):
    ans = "2100-01-01" #设置无穷的时间
    match_re = ".*结束时间:(\d+-\d+-\d+)"
    if re.match(match_re, value):
        ans = re.match(match_re, value).group(1)
    elif re.match(".*结束时间(\d+年\d+月\d+日)", value):
        ans = re.match(".*结束时间(\d+年\d+月\d+日)", value).group(1)
        ans = ans.replace("年", "-")
        ans = ans.replace("月", "-")
        ans = ans.replace("日", "")
    elif re.match(".*截至时间[：为](\d+年\d+月\d+日)", value):
        ans = re.match(".*截至时间[：为](\d+年\d+月\d+日)",value).group(1)
        ans = ans.replace("年", "-")
        ans = ans.replace("月", "-")
        ans = ans.replace("日", "")
    if len(ans) < 5:
        ans = "2100-01-01"
    return ans


def gen_suggestion(index, info_tuple):
    # 根据字符串生成搜索建议数据
    used_words = set()
    suggest = []
    for text, weight in info_tuple:
        if text:
            # 调用es的analyzer的接口对字符串进行分析 analyzer="ik_max_word", analyzer="ik_max_word"
            words = es.indices.analyze(index=index, params={"analyzer": "ik_max_word", "filter": ['lowercase']}, body=text)
            analyzed_list = set([r["token"] for r in words["tokens"] if len(r["token"]) > 1])
            new_words = analyzed_list - used_words
        else:
            new_words = set()
        if new_words:
            suggest.append({"input": list(new_words), "weight":weight})
    return suggest


# 定义一个输出的格式
class BidcontentItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class BidcontentItem(scrapy.Item):
    # 定义了所属的行业（industy），地区（region），资金来源（fund），招标文件名（title），
    # 发布日期（publish_date)，招标文件的url，文章的内容（content）
    industry = scrapy.Field()
    region = scrapy.Field(
        input_processor=MapCompose(get_province)
    )
    fund = scrapy.Field()
    title = scrapy.Field(
        input_processor=MapCompose(remove_tags,get_title)
    )
    publish_date = scrapy.Field(
        input_processor=MapCompose(remove_tags, get_publish_time)
    )
    content = scrapy.Field(
        input_processor=MapCompose(handle_content)
    )
    bid_id = scrapy.Field(
        input_processor=MapCompose(remove_tags, get_bid_id)
    )
    url = scrapy.Field()
    dead_date = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_content, getdeadline)
    )

    def get_insert_sql(self):
        # 主键相同时在更新，没有就插入
        insert_sql = """
                    insert into bid_table(title,url,industry,region,fund,publish_date,content,bid_id,dead_date)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE title=VALUES(title),
                    industry=VALUES(industry),region=VALUES(region),fund=VALUES(fund),
                    publish_date=VALUES(publish_date),content= VALUES(content),bid_id=VALUES(bid_id),
                    dead_date=VALUES(dead_date)
                """
        params = (self['title'], self['url'], self['industry'],
                  self['region'], self['fund'], datetime.datetime.strptime(self['publish_date'], SQL_DATETIME_FORMAT),
                  self['content'], self['bid_id'], datetime.datetime.strptime(self['dead_date'], SQL_DATETIME_FORMAT))
        return insert_sql, params

    def save_to_es(self):
        bid_items = BidType()
        bid_items.title = self['title']
        bid_items.publish_date = self['publish_date']
        bid_items.region = self['region']
        bid_items.industry = self['industry']
        bid_items.bid_id = self['bid_id']
        bid_items.fund = self['fund']
        bid_items.url = self['url']
        bid_items.content = self['content']
        bid_items.dead_date = self['dead_date']
        bid_items.suggestion = gen_suggestion(
            BidType._doc_type.index,
            ((bid_items.title, 10), (bid_items.content, 7)))
        bid_items.save()
        # 将html转成pdf
        HTML_Convert_To_pdf.html_to_pdf(self['url'], STORE_PDF_PATH + self["title"])