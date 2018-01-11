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
    record_price = scrapy.Field()  #历史成交记录
    record_detail = scrapy.Field()  #历史成交记录
    basemore = scrapy.Field()       #房源特色

    #基本属性
    peizhidianti = scrapy.Field()  # 配备电梯
    chanquan = scrapy.Field()  # 产权年限
    tihubili = scrapy.Field()  # 梯户比例
    gongnuan = scrapy.Field()  # 供暖方式
    jianzhujiegou = scrapy.Field()  # 建筑结构
    zhuangxiu = scrapy.Field()  # 装修情况
    jianchengniandai = scrapy.Field()  # 建成年代
    chaoxiang = scrapy.Field()  # 房屋朝向
    jianzhuleixing = scrapy.Field()  # 建筑类型
    taoneimianji = scrapy.Field()  # 套内面积
    huxingjiegou = scrapy.Field()  # 户型结构
    jianzhumianji = scrapy.Field()  # 建筑面积
    louceng = scrapy.Field()  # 所在楼层
    huxing = scrapy.Field()  # 房屋户型

    #交易属性
    bianhao = scrapy.Field()  # 链家编号
    jiaoyiquanshu = scrapy.Field()  # 交易权属
    guapaishijian = scrapy.Field()  # 挂牌时间
    yongtu = scrapy.Field()  # 房屋用途
    fangwunianxian = scrapy.Field()  # 房屋年限
    fangquan = scrapy.Field()  # 房权所属

    #msg
    guapaijiage = scrapy.Field()  # 挂牌价格
    chengjiaozhouqi = scrapy.Field()  # 成交周期
    tiaojia = scrapy.Field()  # 调价
    daikan = scrapy.Field()  # 带看
    guanzhu = scrapy.Field()  # 关注
    liulan = scrapy.Field()  # 浏览
    #pass
