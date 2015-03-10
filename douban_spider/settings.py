# -*- coding: utf-8 -*-

# Scrapy settings for douban_spider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'douban_spider'

SPIDER_MODULES = ['douban_spider.spiders']
NEWSPIDER_MODULE = 'douban_spider.spiders'
ITEM_PIPELINES = ['douban_spider.pipelines.DoubanSpiderPipeline']
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'douban_spider (+http://www.yourdomain.com)'
#end