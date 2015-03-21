# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import  Item,Field
class Book(scrapy.Item):
    title = Field()
    title_english = Field()
    alias = Field()
    authors = Field()
    translator = Field()
    isbn = Field()
    publisher = Field()
    release_year = Field()
    page_num = Field()
    price = Field()
    album = Field()
    douban_url = Field()
    img = Field()
    rating= Field()
    other_info = Field()
    intro = Field()
    content_list = Field()
    #supress logs
    def __str__(self):
        return ""

class BookSnippet(scrapy.Item):
    title = Field()
    url = Field()
    pubinfo = Field()
    img = Field()
    rating = Field()
    reviews = Field()
    #supress logs
    def __str__(self):
        return ""

class DoubanSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
