# -*- coding:utf-8 -*-
import scrapy
import os
import re
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from ..items import QiushibaikeItem
import selenium
from selenium import webdriver
import urllib


class qiushibaike_Spider(scrapy.spiders.Spider):
    name = 'qiushibaike'
    allowed_domains = ['qiushibaike.com']
    start_urls = [
        'http://www.qiushibaike.com',
    ]

    def __init__(self):
        self.browser = webdriver.Firefox()
        self.browser.set_page_load_timeout(30)

    def closed(self,spider):
        print("spider closed")
        self.browser.close()

    def parse(self,response):
        print '**************************** Start labuladuoSpider'
        item = QiushibaikeItem()
        item['duanzi'] = response.xpath('//div[@class="content"]/span/text()').extract()
        item['alt'] = response.xpath('//div[@class="author clearfix"]/a/img/@alt').extract()
        yield item

