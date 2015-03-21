# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.contrib.exporter import JsonItemExporter
from items import Book
from items import BookSnippet
import codecs
import json

class DoubanSpiderPipeline(object):
    def __init__(self):
        file = codecs.open('books2.json','w+b',encoding='utf-8')
        #file = open('books2.json','w+b')
        self.exporter = JsonItemExporter(file)
        self.exporter.encoding='utf-8'
        self.exporter.start_exporting()
        self.encoder = json.JSONEncoder(ensure_ascii=False)

    def spider_closed(self,spider):
        self.exporter.finish_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(self.encoder.encode(item))
        return item

class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.book_store = codecs.open('books.json', 'w', encoding='utf-8')
        self.snippet_store = codecs.open('snippets.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        if isinstance(item,Book):
            return self.process_book(item,spider)
        elif isinstance(item,BookSnippet):
            return self.process_snippet(item,spider)
        else:
            return item

    def process_book(self,item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.book_store.write(line)
        return item

    def process_snippet(self,item,spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.snippet_store.write(line)
        return item

    def spider_closed(self, spider):
        self.book_store.close()
        self.snippet_store.close()