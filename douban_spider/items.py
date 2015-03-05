# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import  Item,Field
class Book(scrapy.Item):
    title = Field()
    isbn = Field()
    authors = Field()
    publisher = Field()
    alias = Field()
    english_name = Field()
    douban_url = Field()
    img = Field()
    publish_date = Field()
    page_num = Field()
    price = Field()
    staring = Field()
    desc = Field()
    content_list = Field()
    tags = Field()

class DoubanSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
