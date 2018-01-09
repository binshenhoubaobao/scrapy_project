# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    region = scrapy.Field()      #行政区域
    href = scrapy.Field()        #房源链接
    name = scrapy.Field()        #房源名称
    style = scrapy.Field()       #房源结构
    area = scrapy.Field()           #小区
    orientation = scrapy.Field()    #朝向
    decoration = scrapy.Field()     #装修
    elevator = scrapy.Field()       #电梯
    floor = scrapy.Field()          #楼层高度
    build_year = scrapy.Field()     #建造时间
    sign_time = scrapy.Field()      #签约时间
    unit_price = scrapy.Field()     #每平米单价
    total_price = scrapy.Field()    #总价
    fangchan_class = scrapy.Field()   #房产类型
    school = scrapy.Field()         #周边学校
    subway = scrapy.Field()         #周边地铁
    msg = scrapy.Field()     #price msg
    base_list = scrapy.Field() #基本属性
    transaction_list = scrapy.Field() #交易属性
    #pass
