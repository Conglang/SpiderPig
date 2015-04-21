# -*- coding: utf-8 -*-
# Filename: pipelines.py
# Find help at 'http://conglang.github.io/2015/04/18/scrapy-huaban-wallpaper/'

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#import scrapy
from scrapy.contrib.pipeline.files import FilesPipeline
#from scrapy.exceptions import DropItem
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from scrapy.http import Request
#import os
from scrapy.utils.misc import md5sum
try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

# Combine item fields into one single url and store it in a xml file.
class HuabanPipeline(object):
    def __init__(self):
        self.doc = ElementTree()
        self.allpic = Element("all_pic")
        self.allpic.tail = '\n'
        self.doc._setroot(self.allpic)

    def process_item(self, item, spider):
        if spider.name == 'huabanSpider':
            url = [item['pin_id'], "http://img.hb.aicdn.com/"+item['key'], item['pic_type'], item['folder']]
            pic = Element('pic')
            pic.tail = '\n'
            self.allpic.append(pic)
            SubElement(pic, 'pin_id').text = url[0]
            SubElement(pic, 'pic_url').text = url[1]
            SubElement(pic, 'pic_type').text = url[2]
            SubElement(pic, 'folder').text = url[3]
            return item

    def close_spider(self, spider):
        if spider.name == 'huabanSpider':
            self.f = open('pic_urls', 'w')
            self.doc.write(self.f)
            self.f.close()

# Another way of download files using FilesPipeline
class DownloadPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        return [Request(x,meta={'item':item}) for x in item.get('file_urls', [])]

    def file_downloaded(self, response, request, info):
        #path = self.file_path(request, response=response, info=info)
        path = response.meta.get('item')['folder'][0] + '/' + response.meta.get('item')['pin_id'][0] + '.' + response.meta.get('item')['pic_type'][0]
        buf = BytesIO(response.body)
        self.store.persist_file(path, buf, info)
        checksum = md5sum(buf)
        return checksum
