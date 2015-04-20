# -*- coding: utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider
from huaban.items import PicItem
import os
import random

# Spider for downloading pictures.
# Grab all picture urls in predefined xml file and store it in item field image_urls.
class downloadSpider(CrawlSpider):
    name = 'downloadSpider'
    allow_domain = ['http://img.hb.aicdn.com/']
    start_urls = []

    def __init__(self, **kw):
        super(downloadSpider, self).__init__(**kw)
        url = kw.get('url') or kw.get('domain') or "pic_urls"
        self.chooseone = kw.get('chooseone')
        url = "file://"+os.path.abspath(".")+"/"+url
        self.start_urls = [url]

    def parse(self, response):
        index = int(0)
        for t in response.xpath("//pic"):
            index = index + 1
        rn = random.randint(0,index-1)
        count = int(0)
        for sel in response.xpath("//pic"):
            item = PicItem()
            item['file_urls'] = sel.xpath("./pic_url/text()").extract()
            item['folder'] = sel.xpath("./folder/text()").extract()
            item['pic_type'] = sel.xpath("./pic_type/text()").extract()
            item['pin_id'] = sel.xpath("./pin_id/text()").extract()
            if rn != count and self.chooseone:
                item['file_urls'] = []
            count = count +1
            yield item

