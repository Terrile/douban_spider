#coding=UTF-8
import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
import string
import re
import math
import urllib
from ..items import Book #this is the way to import code from parent directory
import os
#set default encoding
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class BookSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["douban.com"]
    start_urls = [
        "http://book.douban.com/subject/25752043/"
        #"http://club.jd.com/allconsultations/1258277-2-2.html"
    ]

    def parse(self, response):
        html_txt = response.body.decode("utf-8","ignore")
        hxs = Selector(text=html_txt)
        try:
            #products = hxs.select('//div[@class="lh-wrap"]/div[@class="p-name"]/a/@href')
            book_node = hxs.xpath('//div[@id="wrapper"]')
            title_node = book_node.xpath('.//h1/span/text()')
            #print title_node.extract()[0]
            info_node = book_node.xpath('.//div[@id="info"]')
            info_text = info_node.extract()[0]
            #info_text = re.sub(r"\s+","\s")
            #print info_text
            lines = string.split(info_text,'<br>')
            inbracket = re.compile(r".*<[^<>]+>.*")
            for line in lines:
                line = string.replace(line,'\n','')
                #line = re.sub(inbracket,'',line)
                print line

            test_nodes = info_node.xpath(".//span[@class='pl']/text()")
            for test_node in test_nodes:
                print test_node.extract()
            #print info_node.extract()[0]
            author_node = info_node.xpath('.//div[contains(text(),"作者")]')
            if author_node:
                print "Author"
                print author_node.extract()[0]
            else:
                print "Author Node not found"

            book_title_path = '//div[@id="wrapper"]/h1/span/text()'
            book_title_node = hxs.xpath(book_title_path)
            if book_title_node:
                book_title = book_title_node.extract()[0]
                print book_title
            else:
                print "cannot find book title node"
        except:
            print 'Exception Happened'
            pass

