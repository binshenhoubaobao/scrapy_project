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
        'https://bj.lianjia.com/chengjiao/101102208244.html',
    ]


    def parse(self, response):
        items = LianjiaItem()
        selector = etree.HTML(response.text)
        '''
        #<div class="base"><div class="name">基本属性</div><div class="content"><ul><li><span class="label">房屋户型</span>1室1厅1厨1卫
        # </li><li><span class="label">所在楼层</span>低楼层 (共6层)          </li><li><span class="label">建筑面积</span>36.28㎡
        #  </li><li><span class="label">户型结构</span>平层              </li><li><span class="label">套内面积</span>25.08㎡
        #  </li><li><span class="label">建筑类型</span>板楼       </li><li><span class="label">房屋朝向</span>南
        #  </li><li><span class="label">建成年代</span>1982 </li><li><span class="label">装修情况</span>精装
        #   </li><li><span class="label">建筑结构</span>混合结构  </li><li><span class="label">供暖方式</span>集中供暖
        # </li><li><span class="label">梯户比例</span>一梯三户
        # </li><li><span class="label">产权年限</span>70年           </li><li><span class="label">配备电梯</span>无           </li></ul></div></div>
'''
        base_attribute = {'房屋户型':'huxing','所在楼层':'louceng','建筑面积':'jianzhumianji','户型结构':'huxingjiegou','套内面积':'taoneimianji',
                          '建筑类型':'jianzhuleixing','房屋朝向':'chaoxiang','建成年代':'jianchengniandai','装修情况':'zhuangxiu','建筑结构':'jianzhujiegou',
                          '供暖方式':'gongnuan','梯户比例':'tihubili','产权年限':'chanquan','配备电梯':'peizhidianti'}
        try:
            base_lists = selector.xpath('//div[@class="base"]/div/ul/li/text()')
            base_spans = selector.xpath('//div[@class="base"]/div/ul/li/span/text()')
            base_list = {}
            for i in range(len(base_lists)):
                #print base_spans[i]
                if base_spans[i].encode('utf-8') in base_attribute.keys():
                    #print '**************************************',base_attribute[base_spans[i].encode('utf-8')]
                    element = base_attribute[base_spans[i].encode('utf-8')]
                    items[element] = base_lists[i].strip(' ')
                base_list[base_spans[i]] = base_lists[i].strip(' ')
            items['base_list'] = base_list
        except:
            pass


        # <div class="transaction"><div class="name">交易属性</div><div class="content"><ul><li><span class="label">链家编号</span>101102407859
        # </li><li><span class="label">交易权属</span>已购公房          </li><li><span class="label">挂牌时间</span>2017-12-17
        # </li><li><span class="label">房屋用途</span>普通住宅          </li><li><span class="label">房屋年限</span>暂无数据
        # </li><li><span class="label">房权所属</span>非共有           </li></ul></div></div></div>

        transaction_attribute = {'链家编号':'bianhao','交易权属':'jiaoyiquanshu','挂牌时间':'guapaishijian','房屋用途':'yongtu',
                          '房屋年限':'fangwunianxian','房权所属':'fangquan'}
        try:
            transaction_lists = selector.xpath('//div[@class="transaction"]/div/ul/li/text()')
            transaction_spans = selector.xpath('//div[@class="transaction"]/div/ul/li/span/text()')
            transaction_list = {}
            for i in range(len(transaction_lists)):
                if transaction_spans[i].encode('utf-8') in transaction_attribute.keys():
                    element = transaction_attribute[transaction_spans[i].encode('utf-8')]
                    items[element] = transaction_lists[i].strip(' ')
                transaction_list[transaction_spans[i]] = transaction_lists[i].strip(' ')
            items['transaction_list'] = transaction_list
        except:
            pass


        #历史成交记录
        #<ul class="record_list"><li><span class="record_price" data-signsource="0">529万</span><p class="record_detail">单价71642元/平,链家成交,2017-12-25</p></li><li>
        # <span class="record_price" data-signsource="0">暂无价格</span><p class="record_detail">其他公司成交,2015-09</p></li></ul>
        try:
            items['record_price'] = selector.xpath('//ul[@class="record_list"]/li/span/text()')
            items['record_detail'] = selector.xpath('//ul[@class="record_list"]/li/p/text()')
        except:
            pass


        #房源特色
        #房源标签
        try:
            basemore = {}
            biaoqian = selector.xpath(
                '//div[@class="introContent showbasemore"]/div[@class="tags clear"]/div[@class="name"]/text()')
            biaoqian2s = selector.xpath(
                '//div[@class="introContent showbasemore"]/div[@class="tags clear"]/div[@class="content"]/a/text()')
            basemore[biaoqian[0]] = biaoqian2s

            baseattribute_names = selector.xpath(
                '//div[@class="introContent showbasemore"]/div[@class="baseattribute clear"]/div[@class="name"]/text()')
            baseattribute_contents = selector.xpath(
                '//div[@class="introContent showbasemore"]/div[@class="baseattribute clear"]/div[@class="content"]/text()')
            for i in range(len(baseattribute_names)):
                basemore[baseattribute_names[i]] = baseattribute_contents[i]
            print basemore
            items['basemore'] = basemore
        except:
            pass

#<div class="msg"><span><label>520</label>挂牌价格（万）</span><span><label>68</label>成交周期（天）</span><span><label>0</label>调价（次）</span>
        # <span><label>3</label>带看（次）</span><span><label>11</label>关注（人）</span><span><label>807</label>浏览（次）</span></div>
        #msg

        msg_attribute = {'挂牌价格（万）':'guapaijiage','成交周期（天）':'chengjiaozhouqi','调价（次）':'tiaojia','带看（次）':'daikan',
                          '关注':'guanzhu','浏览（次）':'liulan'}
        try:
            spans = selector.xpath('//div[@class="msg"]/span/text()')
            lb = selector.xpath('//div[@class="msg"]/span/label/text()')
            msg = {}
            for i in range(len(spans)):
                if spans[i].encode('utf-8') in msg_attribute.keys():
                    element = msg_attribute[spans[i].encode('utf-8')]
                    items[element] = lb[i].strip(' ')
                msg[spans[i]] = lb[i]
            # print msg
            items['msg'] = msg
        except:
            pass
        yield items






