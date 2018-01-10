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
    start_urls = [
        'https://bj.lianjia.com/chengjiao/101102157235.html',
    ]


    def parse(self, response):
        print '!!!!!!!!!!!!!!!!!!!!!!!!!!'
        items = LianjiaItem()
        selector = etree.HTML(response.text)
        #<div class="base"><div class="name">基本属性</div><div class="content"><ul><li><span class="label">房屋户型</span>1室1厅1厨1卫
        # </li><li><span class="label">所在楼层</span>低楼层 (共6层)          </li><li><span class="label">建筑面积</span>36.28㎡
        #  </li><li><span class="label">户型结构</span>平层              </li><li><span class="label">套内面积</span>25.08㎡
        #  </li><li><span class="label">建筑类型</span>板楼       </li><li><span class="label">房屋朝向</span>南
        #  </li><li><span class="label">建成年代</span>1982 </li><li><span class="label">装修情况</span>精装
        #   </li><li><span class="label">建筑结构</span>混合结构  </li><li><span class="label">供暖方式</span>集中供暖
        # </li><li><span class="label">梯户比例</span>一梯三户
        # </li><li><span class="label">产权年限</span>70年           </li><li><span class="label">配备电梯</span>无           </li></ul></div></div>



        base_lists = selector.xpath('//div[@class="base"]/div/ul/li/text()')
        base_spans = selector.xpath('//div[@class="base"]/div/ul/li/span/text()')
        base_list = {}
        for i in range(len(base_lists)):
            base_list[base_spans[i]] = base_lists[i]
        items['base_list'] = base_list

        # <div class="transaction"><div class="name">交易属性</div><div class="content"><ul><li><span class="label">链家编号</span>101102407859
        # </li><li><span class="label">交易权属</span>已购公房          </li><li><span class="label">挂牌时间</span>2017-12-17
        # </li><li><span class="label">房屋用途</span>普通住宅          </li><li><span class="label">房屋年限</span>暂无数据
        # </li><li><span class="label">房权所属</span>非共有           </li></ul></div></div></div>
        transaction_lists = selector.xpath('//div[@class="transaction"]/div/ul/li/text()')
        transaction_spans = selector.xpath('//div[@class="transaction"]/div/ul/li/span/text()')
        transaction_list = {}
        for i in range(len(transaction_lists)):
            transaction_list[transaction_spans[i]] = transaction_lists[i]
        items['transaction_list'] = transaction_list

        #历史成交记录
        #<ul class="record_list"><li><span class="record_price" data-signsource="0">529万</span><p class="record_detail">单价71642元/平,链家成交,2017-12-25</p></li><li>
        # <span class="record_price" data-signsource="0">暂无价格</span><p class="record_detail">其他公司成交,2015-09</p></li></ul>
        items['record_price'] = selector.xpath('//ul[@class="record_list"]/li/span/text()')
        items['record_detail'] = selector.xpath('//ul[@class="record_list"]/li/p/text()')



        yield items





