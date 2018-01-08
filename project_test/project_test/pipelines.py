# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ProjectTestPipeline(object):
    def process_item(self, item, spider):
        return item


class SaveCnblog_Pipeline(object):
    '''
    实现保存到txt文件的类，类名这个地方为了区分，做了修改，
    当然这个类名是什么并不重要，你只要能区分就可以，
    请注意，这个类名待会是要写到settings.py文件里面的。
    '''
    def process_item(self, item, spider):
        with open('/home/kali/PycharmProjects/scrapy_project/project_test/duanzi.txt', 'w') as f:
            titles = item['alt']
            links = item['duanzi']
            for i, j in zip(titles, links):
                str = i + ':' + j + '\n'
                f.write(str.encode('utf-8'))
        return item



