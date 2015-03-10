# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.contrib.exporter import JsonItemExporter
import json
class DoubanSpiderPipeline(object):
    def __init__(self):
        file = open('books2.json','w+b')
        self.exporter = JsonItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self,spider):
        self.exporter.finish_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item