# -*- coding: utf-8 -*-
'''
    这段主要用来抓取省份和所有的行业，并且存入数据表中
'''
import requests
from scrapy.selector import Selector
import MySQLdb
import re

conn = MySQLdb.connect(host="localhost", db="bid_spider", user="root", passwd="123456", charset="utf8")
cursor = conn.cursor()

headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
}

url = 'http://www.chinabidding.com/search/proj.htm'
response = requests.get(url, headers=headers)
ans = response.text
nums = 1
selector = Selector(text=ans)
# 用来抓取省份
# def get_province():
#     # 获得省份并插入数据库
#     pro_lis = selector.css("#zoneCode option")
#     pro_lists = []
#     for option in pro_lis:
#         pro = option.css("::text").extract()[0]
#         ans = re.match(".*--(.*)", str(pro), re.DOTALL)
#         province = ""
#         if ans:
#             province = ans.group(1)
#             insert_sql = """
#                   insert into province_table(id,province_name) VALUES (%s,%s)
#             """
#             cursor.execute(insert_sql, (nums, str(province)))
#             conn.commit()
#             nums += 1
# get_province()


# 获取行业并存入数据库
def get_industry():
    nums = 1
    industry_lis = selector.css("#normIndustry option")
    for option in industry_lis[1:]:
        industry = option.css("::text").extract()[0]
        insert_sql = """
              insert into industry_table(id,industry_name) VALUES (%s,%s)
        """
        cursor.execute(insert_sql, (nums, str(industry)))
        conn.commit()
    nums += 1

get_industry()