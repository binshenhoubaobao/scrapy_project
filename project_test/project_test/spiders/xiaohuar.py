# -*- coding:utf-8 -*-
import scrapy
import os
import re
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from ..items import XiaohuaItem
#from project_test.items import JiandanItem
import urllib


class XiaoHuarSpider(scrapy.spiders.Spider):
    name = "xiaohua"
    allowed_domains = ["xiaohuar.com"]
    start_urls = [
        "http://www.xiaohuar.com/hua/",
    ]

    def parse(self, response):
        # print(response, type(response))
        # from scrapy.http.response.html import HtmlResponse
        # print(response.body_as_unicode())

        current_url = response.url  # 爬取时请求的url
        body = response.body  # 返回的html
        unicode_body = response.body_as_unicode()  # 返回的html unicode编码

        # 分析页面
        # 找到页面中符合规则的内容（校花图片），保存
        # 找到所有的a标签，再访问其他a标签，一层一层的搞下去

        hxs = HtmlXPathSelector(response)  # 创建查询对象
        # 获取所有的url，继续访问，并在其中寻找相同的url
        all_urls = hxs.select('//a/@href').extract()
        for url in all_urls:
            if url.startswith('http://www.xiaohuar.com/list-1-'):
                print '*****************start  XiaoHuarSpider url:',url
                yield Request(url, callback=self.parse)

        # 如果url是 http://www.xiaohuar.com/list-1-\d+.html
        if re.match('http://www.xiaohuar.com/list-1-\d+.html', response.url):  # 如果url能够匹配到需要爬取的url，即本站url
            xiaohuaitem = XiaohuaItem()
            src = hxs.select(
                '//div[@class="img"]/a/img/@src').extract()  # 查询所有img标签的src属性，即获取校花图片地址
            name = hxs.select(
                '//div[@class="img"]/span/text()').extract()  # 获取span的文本内容，即校花姓名
            school = hxs.select(
                '//div[@class="img"]/div[@class="btns"]/a/text()').extract()  # 校花学校

            xiaohuaitem['src'] = src
            xiaohuaitem['school'] = school
            xiaohuaitem['name'] = name
            yield xiaohuaitem

