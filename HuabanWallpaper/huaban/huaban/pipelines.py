# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

'''
def check_spider_pipeline(process_item_method):

    @functools.wraps(process_item_method)
    def wrapper(self, item, spider):

        # message template for debugging
        msg = '%%s %s pipeline step' % (self.__class__.__name__,)

        # if class is in the spider's pipeline, then use the
        # process_item method normally.
        if self.__class__ in spider.pipeline:
            #spider.log(msg % 'executing', level=log.DEBUG)
            return process_item_method(self, item, spider)

        # otherwise, just return the untouched item (skip this step in
        # the pipeline)
        else:
            #spider.log(msg % 'skipping', level=log.DEBUG)
            return item

    return wrapper
'''

# Combine item fields into one single url and store it in a xml file.
class HuabanPipeline(object):
    def __init__(self):
        self.doc = ElementTree()
        self.allpic = Element("all_pic")
        self.allpic.tail = '\n'
        self.doc._setroot(self.allpic)
        self.isopen = False

    def process_item(self, item, spider):
        if spider.name == 'huabanSpider':
            if not self.isopen:
                folder = 'pic_urls'
                self.file = open(folder, 'w')
                self.isopen = True
            url = [item['pin_id'], "http://img.hb.aicdn.com/"+item['key'],item['pictype']]
            pic = Element('pic')
            pic.tail = '\n'
            self.allpic.append(pic)
            SubElement(pic, 'pin_id').text = url[0]
            SubElement(pic, 'pic_url').text = url[1]
            return item

    def close_spider(self, spider):
        if spider.name == 'huabanSpider':
            self.doc.write(self.file)
            self.file.close()


# Download picture in item field image_urls.
class DownloadPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item and item['image_urls']:
            url = item['image_urls']
            yield scrapy.Request(url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item
