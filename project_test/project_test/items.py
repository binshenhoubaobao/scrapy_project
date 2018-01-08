# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProjectTestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CnblogItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()

class JiandanItem(scrapy.Item):
    image_urls = scrapy.Field()#图片的链接
    images = scrapy.Field()
    img_hash = scrapy.Field()

class QiushibaikeItem(scrapy.Item):
    duanzi = scrapy.Field()
    alt = scrapy.Field()

class XiaohuaItem(scrapy.Item):
    # define the fields for your item here like:
    img_url = scrapy.Field()
    name = scrapy.Field()
    school = scrapy.Field()
    src = scrapy.Field()