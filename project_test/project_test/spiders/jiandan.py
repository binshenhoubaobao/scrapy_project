# -*- coding:utf-8 -*-
import scrapy
import os
import re
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from project_test.items import JiandanItem
import urllib


class JiandanSpider(scrapy.spiders.Spider):
    name = 'jiandan'
    start_urls = ["http://jandan.net/ooxx"]

    def parse(self, response):

        item = JiandanItem()
        item['image_urls'] = response.xpath('//img//@src').extract() #提取图片链接
        item['img_hash'] = response.xpath('//span[@class="img-hash"]/text()').extract() #提取图片链接span class ="img-hash"
        yield item
