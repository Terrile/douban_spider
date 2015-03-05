# -*- coding: utf-8 -*-
__author__ = 'Administrator'
from scrapy.spider import  BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
import re
import math
import urllib

from ..items import Book

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class BookSpider(BaseSpider):
    name = "DBS" #DBS: abbr for Douban Book Spider
    start_urls = ["http://book.douban.com/subject/5320866/"]

    def parse(self,response):
        html_txt = response.body.decode("utf-8","ignore")
        hxs = Selector(text=html_txt)
       # print html_txt
        try:
            title = hxs.xpath('//div[@id="wrapper"]/h1/span/text()')
            print title.extract()[0]
            info_s = hxs.xpath('//div[@class="intro"]/p/')
            for info in info_s:
                text = info.xpath("text()").extract()[0]
                print text
            #title = hxs.xpath('//div[@class="intro"]/text()')
           # print 'Book title: '+title
        except:
            print 'failed to parse url'
