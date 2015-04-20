# -*- coding: utf-8 -*-

from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider
from huaban.items import HuabanItem
import re
import time

# Spider for parsing user-defined board page.
class huabanSpider(CrawlSpider):
    # name of spider
    name = 'huabanSpider'
    allow_domain = ['huaban.com']
    start_urls = []
    last_num = "000000000"

    # get start_url from user input.
    def __init__(self, **kw):
        super(huabanSpider, self).__init__(**kw)
        url = kw.get('url') or kw.get('domain') or 'http://huaban.com/boards/344630/'
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://%s/' % url
        #self.log(url)
        self.start_urls = [url]

    # Decimal to hexadecimal thirty-six to generate uniqueid in jquery.
    def ten_to_thirtysix(self, num):
        loop = '0123456789abcdefghijklmnopqrstuvwxyz'
        result = []
        num = int(num)
        while num != 0:
            i = num % 36
            result.append(loop[int(i)%36])
            num = num / 36
        result.reverse()
        return ''.join(result)

    # Load more content at the end of current page by sending jquery.
    def load_more(self, url, no):
        milliseconds = time.time()+1
        uniqueid = str(self.ten_to_thirtysix(milliseconds))
        resulturl = '%s' % str(url+"?"+uniqueid+"&max="+self.last_num+"&limit=20&wfl=1")
        return resulturl

    # Parse javascript strings under xpath script using regex.
    def parse(self, response):
        '''
        Ugly Code!
        What is the best practice of checking value's validation in python?
        Please help!
        '''
        for sel in response.xpath('//script').re("\{\"pin_id.*?hide_origin.*?\}"):
            item = HuabanItem()
            item['folder'] = response.url.split("/")[-2]
            # get pin id
            spinid = re.findall(u"pin_id..\d*", sel)
            if spinid and spinid[0]:
                sspinid = spinid[0].split(":")
                if sspinid:
                    self.last_num = sspinid[-1]
                    item['pin_id'] = self.last_num
            # get key
            skey = re.findall(u"key\":\"\w+-\w+\"", sel)
            if skey and skey[0]:
                sskey = skey[0].split("\"")
                if sskey:
                    item['key'] = sskey[-2]
            # get pictype
            spictype = re.findall(u"type\":\"\w+/.+?\"", sel)
            if spictype and spictype[0]:
                sspictype = spictype[0].split("\"")
                if sspictype:
                    ssipictype = sspictype[-2]
                    if ssipictype:
                        ssspictype = ssipictype.split("/")
                        if ssspictype:
                            item['pic_type'] = ssspictype[-1]
            yield item

        yield Request(url = self.load_more(self.start_urls[0], self.last_num), callback = self.parse)

