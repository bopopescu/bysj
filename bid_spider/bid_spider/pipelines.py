# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
# from tools import HTML_Convert_To_pdf
from .modes.es_type import BidType
import datetime


class BidSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


# 保存导数据库 mysql数据库的连接存储
class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings): #读取setting里面的值，
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用Twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)
        # 处理异常

    def handle_error(self, failure):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)


# 将数据写入到elasticsearch中，形成全文检索所需要的字典
# python的elasticsearch的接口 elasticsearch-dsl
class ElasticsearchPipeline(object):

    def process_item(self, item, spider):
        item.save_to_es()
        return item
