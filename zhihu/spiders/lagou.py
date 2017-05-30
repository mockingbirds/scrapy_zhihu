# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from items import LagouJobItem, LagouJobItemLoader
from spiders.utils.common import get_md5
import datetime

class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    rules = (
        #https://www.lagou.com/gongsi/j9891.html  follow表示深度解析，即当前页面的所有子页面
        Rule(LinkExtractor(allow=r'gongsi/j\d.html',), follow=True),
        #https://www.lagou.com/zhaopin/Java/?labelWords=label
        Rule(LinkExtractor(allow=r'zhaopin/.*',), follow=True),
        #https://www.lagou.com/jobs/2785439.html   如果当前url是jobs/\d+.html格式的，则回调parse_item进行具体的解析动作
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        #解析拉勾网职位
        lagouItemLoader = LagouJobItemLoader(item=LagouJobItem(), response=response)
        lagouItemLoader.add_css('title', '.job-name span::text')
        lagouItemLoader.add_value('url', response.url)
        lagouItemLoader.add_value('url_obj_id', get_md5(response.url))
        lagouItemLoader.add_css('salary', '.job_request .salary ::text')
        lagouItemLoader.add_xpath('job_city', '//dd[@class="job_request"]/p/span[2]/text()')
        lagouItemLoader.add_xpath('work_years', '//dd[@class="job_request"]/p/span[3]/text()')
        lagouItemLoader.add_xpath('degree_need', '//dd[@class="job_request"]/p/span[4]/text()')
        lagouItemLoader.add_xpath('job_type', '//dd[@class="job_request"]/p/span[5]/text()')

        lagouItemLoader.add_css('tags', '.position-label li::text')
        lagouItemLoader.add_css('publish_time', '.publish_time::text')
        lagouItemLoader.add_css('job_advantage', '.job-advantage p::text')
        lagouItemLoader.add_css('job_desc', '.job_bt div')
        lagouItemLoader.add_css('job_addr', '.work_addr')
        lagouItemLoader.add_css('company_url', '#job_company a::attr(href)')
        lagouItemLoader.add_css('company_name', '#job_company img::attr(alt)')
        lagouItemLoader.add_value('craw_time', datetime.datetime.now().date())
        lagouItemLoader.add_value('craw_update_time', '')

        lagouJobItem = lagouItemLoader.load_item()
        print(lagouJobItem)
        return lagouJobItem
