# -*- coding:utf-8 -*-
import scrapy

from scrapy import Spider,Request
import re
from lxml import etree
import json



class Lianjia_test_Spider(scrapy.spiders.Spider):
    name = 'lianjiatest'
    allowed_domains = ['nj.lianjia.com']
    regions = {'xicheng':'北京西城成交二手房',
               'chaoyang':'北京朝阳成交二手房'
    }

    def start_requests(self):
        for region in list(self.regions.keys()):
            url = "https://bj.lianjia.com/xiaoqu/" + region + "/"
            yield Request(url=url, callback=self.parse, meta={'region':region}) #用来获取页码

    def parse(self, response):
        region = response.meta['region']
        selector = etree.HTML(response.text)
        sel = selector.xpath("//div[@class='page-box house-lst-page-box']/@page-data")[0]  # 返回的是字符串字典
        sel = json.loads(sel)  # 转化为字典
        total_pages = sel.get("totalPage")
        print 'total_pages:',total_pages
        if total_pages >3:
            total_pages = 2

        for i in range(int(total_pages)):
            url_page = "https://bj.lianjia.com/chengjiao/{}/pg{}".format(region, str(i+1))
            yield Request(url=url_page, callback=self.parse_content, meta={'region':region})

    def parse_content(self, response):
        selector = etree.HTML(response.text)
        region = response.meta['region']
        print 'region: ',region
        try:
            house_url = selector.xpath('//div[@class="info"]/div[@class="title"]/a/@href')
            print house_url
            yield house_url
        except:
            pass



