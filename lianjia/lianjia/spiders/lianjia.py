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
        print 'total_pages:',total_pages
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
            base_list[base_spans[i].strip(' ')] = base_lists[i].strip(' ')
        items['base_list'] = base_list

        # <div class="transaction"><div class="name">交易属性</div><div class="content"><ul><li><span class="label">链家编号</span>101102407859
        # </li><li><span class="label">交易权属</span>已购公房          </li><li><span class="label">挂牌时间</span>2017-12-17
        # </li><li><span class="label">房屋用途</span>普通住宅          </li><li><span class="label">房屋年限</span>暂无数据
        # </li><li><span class="label">房权所属</span>非共有           </li></ul></div></div></div>
        transaction_lists = selector.xpath('//div[@class="transaction"]/div/ul/li/text()')
        transaction_spans = selector.xpath('//div[@class="transaction"]/div/ul/li/span/text()')
        transaction_list = {}
        for i in range(len(transaction_lists)):
            transaction_list[transaction_spans[i].strip(' ')] = transaction_lists[i].strip(' ')
        items['transaction_list'] = transaction_list

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


        spans = selector.xpath('//div[@class="msg"]/span/text()')
        lb = selector.xpath('//div[@class="msg"]/span/label/text()')
        msg = {}
        for i in range(len(spans)):
            msg[spans[i]] = lb[i]
        #print msg
        items['msg'] = msg

        yield items
