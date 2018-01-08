# -*- coding:utf-8 -*-
import scrapy
import os
import re
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from ..items import XiaohuaItem
import urllib


class XiaoHuarSpider(scrapy.spiders.Spider):
    name = "xiaohua"
    allowed_domains = ["xiaohuar.com"]
    start_urls = [
        "http://www.xiaohuar.com/list-1-4.html",
    ]

    def parse(self, response):
        # print(response, type(response))
        # from scrapy.http.response.html import HtmlResponse
        # print(response.body_as_unicode())
        hxs = HtmlXPathSelector(response)  # 创建查询对象
        print '*****************start  XiaoHuarSpider re'
        # items = hxs.select('//div[@class="item_list infinite_scroll"]/div')  # select中填写查询目标，按scrapy查询语法书写
        items = XiaohuaItem()
        src = hxs.select(
            '//div[@class="img"]/a/img/@src').extract()  # 查询所有img标签的src属性，即获取校花图片地址
        name = hxs.select(
            '//div[@class="img"]/span/text()').extract()  # 获取span的文本内容，即校花姓名
        school = hxs.select(
            '//div[@class="img"]/div[@class="btns"]/a/text()').extract()  # 校花学校

        items['src'] = src
        items['school'] = school
        items['name'] = name
        yield items