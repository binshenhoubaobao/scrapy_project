# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import DropItem
import os
from scrapy.pipelines.images import ImagesPipeline   #内置的图片管道
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class XiaohuaPipeline(ImagesPipeline):#继承ImagesPipeline这个类
    def process_item(self, item, spider):
        def get_media_requests(self, item, info):
            for image_url in item['img_url']:
                image_url = "http://www.xiaohuar.com" + image_url
                yield scrapy.Request(image_url)

        def item_completed(self, results, item, info):
            image_paths = [x['path'] for ok, x in results if ok]
            #if not image_paths:
            #    raise DropItem("Item contains no images")
            if not image_paths:
                raise DropItem("Item contains no images")
            if item['school']:
                newname = item['school'].encode('utf-8') + '_' + item['name'].encode('utf-8') + '.jpg'
            else:
                newname = item['img_url']  + '.jpg'
            #os.rename(image_paths[0],newname)
            return item

