# -*- coding: utf-8 -*-
# Filename: items.py
# Find help at 'http://conglang.github.io/2015/04/18/scrapy-huaban-wallpaper/'

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
    pic_type = Field()

# Item to download picture.
class PicItem(scrapy.Item):
    file_urls = Field()
    files = Field()
    folder = Field()
    pic_type = Field()
    pin_id = Field()
