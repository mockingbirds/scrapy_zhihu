# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ZhihuPipeline(object):
    def process_item(self, item, spider):
        return item


from twisted.enterprise import adbapi
import MySQLdb.cursors
import MySQLdb

class MyTwistedPipeline(object):
    def __init__(self, dbpool):
        # 在执行完from_settings之后,将dbpool初始化
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings["MYSQL_HOST"],
            port=settings["MYSQL_PORT"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PWD"],
            db=settings["MYSQL_DB"],
            charset=settings["MYSQL_CHARSET"],
            use_unicode=settings["MYSQL_USER_UNICODE"],
            cursorclass=MySQLdb.cursors.DictCursor,
        )
        # 这里通过adbapi构造一个dbpool，并传入MyTwistedPipeline的构造方法
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted异步插入数据到mysql
        query = self.dbpool.runInteraction(self.insert_data, item)
        query.addErrback(self.handle_error)

    def handle_error(self,failure):
        # 处理异步插入异常
        print(failure)

    def insert_data(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        print(insert_sql, params)
        cursor.execute(insert_sql, params)