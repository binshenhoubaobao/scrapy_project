# -*- coding:utf-8 -*-
import scrapy

from scrapy import Spider,Request
import re
from lxml import etree
from ..items import LianjiaItem
import json

class Lianjia_test2_Spider(scrapy.spiders.Spider):
    name = 'lianjiatest2'
    allowed_domains = ['bj.lianjia.com']
    start_urls = [
        'https://bj.lianjia.com/chengjiao/101102208244.html',
    ]

    def parse(self, response):
        items = LianjiaItem()

        selector = etree.HTML(response.text)
        #房源特色
        #房源标签
        basemore = {}
        biaoqian = selector.xpath('//div[@class="introContent showbasemore"]/div[@class="tags clear"]/div[@class="name"]/text()')
        biaoqian2s = selector.xpath('//div[@class="introContent showbasemore"]/div[@class="tags clear"]/div[@class="content"]/a/text()')
        basemore[biaoqian[0]] = biaoqian2s

        baseattribute_names = selector.xpath(
            '//div[@class="introContent showbasemore"]/div[@class="baseattribute clear"]/div[@class="name"]/text()')
        baseattribute_contents = selector.xpath(
            '//div[@class="introContent showbasemore"]/div[@class="baseattribute clear"]/div[@class="content"]/text()')
        for i in range(len(baseattribute_names)):
            basemore[baseattribute_names[i]] = baseattribute_contents[i]
        print basemore
        items['basemore'] = basemore
        yield items