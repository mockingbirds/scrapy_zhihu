# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags

class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

from scrapy.loader import ItemLoader


class LagouJobItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


# 移除'/广州 / 经验3-5年 / 本科及以上 /'中的/
def replace_splash(value):
    return value.replace("/", "")


# 工作地址的处理 ‘广州 - 天河区 - 天河城 - 体育中心103号维多利广场B塔32F   查看地图’
def handle_jobaddr(value):
    addr_list = value.split("\n")
    addr_list = [item.strip() for item in addr_list if item.strip() != "查看地图"]
    return "".join(addr_list)


class LagouJobItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    url_obj_id = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(
        input_processor=MapCompose(replace_splash)
    )
    work_years = scrapy.Field(
        input_processor=MapCompose(replace_splash)
    )
    degree_need = scrapy.Field(
        input_processor=MapCompose(replace_splash)
    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    tags = scrapy.Field(
        input_processor=Join(',')
    )
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field(
        # 移除html标签
        input_processor=MapCompose(remove_tags)
    )
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_jobaddr)
    )
    company_url = scrapy.Field()
    company_name = scrapy.Field()
    craw_time = scrapy.Field()
    craw_update_time = scrapy.Field()

    #重写get_insert_sql方法，该方法会在MyTwistedPipeline中调用，执行存储操作
    def get_insert_sql(self):
        insert_sql = """
            insert into lagou_table(url, url_obj_id, title, salary, job_city,
                work_years, degree_need, job_type, publish_time, tags, job_advantage,
                job_desc, job_addr, company_url, company_name
            ) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE job_desc=VALUES(job_desc)
        """

        params = (
            self['url'], self['url_obj_id'], self['title'], self['salary'] , self['job_city'],
                self['work_years'], self['degree_need'], self['job_type'], self['publish_time'],
                self['tags'], self['job_advantage'],self['job_desc'], self['job_addr'],
                self['company_url'], self['company_name']
        )
        return insert_sql, params