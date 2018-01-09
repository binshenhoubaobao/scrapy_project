# -*- coding:utf-8 -*-
import scrapy

from scrapy import Spider,Request
import re
from lxml import etree
from ..items import LianjiaItem
import json



class Lianjia_test_Spider(scrapy.spiders.Spider):
    name = 'lianjiatest'
    allowed_domains = ['bj.lianjia.com']
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
            total_pages = 1

        for i in range(int(total_pages)):
            url_page = "https://bj.lianjia.com/chengjiao/{}/pg{}".format(region, str(i+1))
            #url_page1 = 'https://bj.lianjia.com/chengjiao/chaoyang/'
            yield Request(url=url_page, callback=self.parse_house_url, meta={'region':region})

    def parse_house_url(self, response):
        items = LianjiaItem()
        selector = etree.HTML(response.text)
        region = response.meta['region']
        #print 'region: ',region
        house_url = selector.xpath('//div[@class="info"]/div[@class="title"]/a/@href')
        for i in range(len(house_url)):
            # print house_url
            yield Request(url=house_url[i], callback=self.parse_hourse_info, meta={'region': region, 'href': house_url})



    def parse_hourse_info(self,response):
        items = LianjiaItem()
        selector = etree.HTML(response.text)
        items['region'] = response.meta['region']
        items['href'] = response.meta['href']
        try:
            #<div class="price"><span class="dealTotalPrice"><i>300</i>万</span><b>82691</b>元/平</div>
            dealTotalPrice1 = selector.xpath('//div[@class="price"]/span/text()')[0]
            dealTotalPrice2 = selector.xpath('//span[@class="dealTotalPrice"]/i/text()')[0]
            print dealTotalPrice1
            print dealTotalPrice2
        except:
            print 'dealTotalPrice error!!'

        msg = {}
        spans = selector.xpath('//div[@class="msg"]/span/text()')
        lb = selector.xpath('//div[@class="msg"]/span/label/text()')
        for i in range(len(spans)):
            msg[spans[i]] = lb[i]
        print msg





