# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field

# Item to store picture url info.
class HuabanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    folder = Field()
    pin_id = Field()
    key = Field()
    pictype = Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()

# Item to download picture.
class PicItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
