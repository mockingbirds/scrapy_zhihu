# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from spiders.utils.common import extract_num


class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags


class LagouJobItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

# def replace_splash(value):
#     return value.replace("/", "")
#
#
# def handle_strip(value):
#     return value.strip()
#
#
# def handle_jobaddr(value):
#     addr_list = value.split("\n")
#     addr_list = [item.strip() for item in addr_list if item.strip() != "查看地图"]
#     return "".join(addr_list)


class LagouJobItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    url_obj_id = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field()
    work_years = scrapy.Field()
    degree_need = scrapy.Field()
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    tags = scrapy.Field()
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field()
    job_addr = scrapy.Field()
    company_url = scrapy.Field()
    company_name = scrapy.Field()
    craw_time = scrapy.Field()
    craw_update_time = scrapy.Field()