# -*- coding:utf-8 -*-
import scrapy
from scrapy import Spider,Request
import re
from lxml import etree
from ..items import LianjiaItem
import json



class LianjiaSpider(scrapy.spiders.Spider):
    name = 'lianjia'
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
        #print 'total_pages:',total_pages
        #
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
            yield Request(url=house_url[i], callback=self.parse_hourse_info, meta={'region': region, 'href': house_url[i]})



    def parse_hourse_info(self,response):
        items = LianjiaItem()
        selector = etree.HTML(response.text)
        items['region'] = response.meta['region']
        items['href'] = response.meta['href']
        items['name'] = selector.xpath('//head/title/text()')

        #<div class="base"><div class="name">基本属性</div><div class="content"><ul><li><span class="label">房屋户型</span>1室1厅1厨1卫
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

        #dealTotalPrice
        try:
            #<div class="price"><span class="dealTotalPrice"><i>300</i>万</span><b>82691</b>元/平</div>
            dealTotalPrice1 = selector.xpath('//div[@class="price"]/span/text()')[0]
            dealTotalPrice2 = selector.xpath('//span[@class="dealTotalPrice"]/i/text()')[0]
            unit_price = selector.xpath('//div[@class="price"]/b/text()')
            items['unit_price'] = unit_price
            items['total_price'] = dealTotalPrice2
            #print selector.xpath('//div[@class="price"]/text()')
            #print unit_price
        except:
            print 'dealTotalPrice error!!'

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

        #历史成交记录
        #<ul class="record_list"><li><span class="record_price" data-signsource="0">529万</span><p class="record_detail">单价71642元/平,链家成交,2017-12-25</p></li><li>
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
                basemore[baseattribute_names[i].strip()] = baseattribute_contents[i].strip()
            #print basemore
            items['basemore'] = basemore
        except:
            pass


        yield items
