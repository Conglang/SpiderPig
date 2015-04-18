# -*- coding: utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider
from huaban.items import PicItem
#from huaban.pipelines import DownloadPipeline
import os
import random

# Spider for downloading pictures.
# Grab all picture urls in predefined xml file and store it in item field image_urls.
class downloadSpider(CrawlSpider):
    name = 'downloadSpider'
    allow_domain = ['http://img.hb.aicdn.com/']
    start_urls = []
    #pipeline = set([
        #DownloadPipeline
    #])

    def __init__(self, **kw):
        super(downloadSpider, self).__init__(**kw)
        url = kw.get('url') or kw.get('domain') or "pic_urls"
        self.chooseone = kw.get('chooseone')
        url = "file://"+os.path.abspath(".")+"/"+url
        self.start_urls = [url]

    def parse(self, response):
        index = int(0)
        for t in response.xpath("//all_pic").xpath("//pic_url"):
            index = index + 1
        rn = random.randint(0,index-1)
        count = int(0)
        for sel in response.xpath("//all_pic").xpath("//pic_url"):
            item = PicItem()
            item['image_urls'] = sel.xpath("./text()").extract()
            if rn != count and self.chooseone:
                item['image_urls'] = ''
            count = count +1
            yield item

