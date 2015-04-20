# -*- coding: utf-8 -*-

# Scrapy settings for huaban project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'huaban'

SPIDER_MODULES = ['huaban.spiders']
NEWSPIDER_MODULE = 'huaban.spiders'
ITEM_PIPELINES = {
    'huaban.pipelines.DownloadPipeline':2,
    'huaban.pipelines.HuabanPipeline':3
}

FILES_STORE = 'pic'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'huaban (+http://www.yourdomain.com)'
