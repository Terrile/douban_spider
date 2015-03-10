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
#import pprint
from pprint import pprint
reload(sys)
sys.setdefaultencoding('utf-8')

class BookSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["douban.com"]
    start_urls = [
        #"http://book.douban.com/subject/25752043/"
        u'http://book.douban.com/tag/%E4%BA%92%E8%81%94%E7%BD%91?start=0&type=T'
    ]

    def parse(self, response):
        html_txt = response.body.decode("utf-8","ignore")
        url = response.url
        hxs = Selector(text=html_txt)
        try:
            #items = hxs.xpath('//ul[@class="subject-list"]/li[@class="subject-item"]/info/h2/a/@href')
            items = hxs.xpath('//ul[@class="subject-list"]/li[@class="subject-item"]/div/h2/a/@href')
            if items:
                for item in items:
                    yield Request(url=item.extract(),callback=self.parse_book)
                m = re.search(r'start=(\d+)',url)
                if m:
                    page_no = int(m.group(1)) + 1
                    print 'Page: '+ str(page_no)+' is processed'
                    next_page = u'http://book.douban.com/tag/%E4%BA%92%E8%81%94%E7%BD%91?start='+str(page_no)+u'&type=T'
                    yield Request(url=next_page,callback=self.parse)
                else:
                    print 'invalid input url'
            else:
                print 'not find items'
        except Exception,e:
            print e
            raise

    def parse_book(self, response):
        html_txt = response.body.decode("utf-8","ignore")
        hxs = Selector(text=html_txt)
        book = Book()
        try:
            book_node = hxs.xpath('//div[@id="wrapper"]')
            title_node = book_node.xpath('.//h1/span/text()')
            info_node = book_node.xpath('.//div[@id="info"]')
            info_text = info_node.extract()[0]
            lines = string.split(info_text,'<br>')
            inbracket = re.compile(r"<[^<>]+>")
            for line in lines:
                line = string.replace(line,'\n','')
                line = re.sub(inbracket,'',line)
                line = re.sub(r'\s+',' ',line)
                field,value = self.extract_info(line)
                if field==u'作者':
                    book['authors'] = value
                elif field==u'出版社':
                    book['publisher'] = value
                elif field==u'原作名':
                    book['title_english'] = value
                elif field==u'译者':
                    book['translator'] = value
                elif field==u'出版年':
                    book['publisher'] = value
                elif field==u'页数':
                    book['page_num'] = value
                elif field==u'定价':
                    book['price'] = value
                elif field==u'丛书':
                    book['album'] = value
                elif field=='ISBN':
                    book['isbn'] = value
                else:
                    if field!="" and value!="":
                        book['other_info'] = field+":"+value

            rating_node = book_node.xpath('.//div[@id="interest_sectl"]/div/p/strong/text()')
            if rating_node:
                book['rating'] = string.strip(rating_node.extract()[0])
            else:
                print "score node not found"


            book_title_path = '//div[@id="wrapper"]/h1/span/text()'
            book_title_node = hxs.xpath(book_title_path)
            if book_title_node:
                book['title'] = book_title_node.extract()[0]
            else:
                print "cannot find book title node"

            img_path = '//div[@id="mainpic"]/a/img/@src'
            img_node = hxs.xpath(img_path)
            if img_node:
                img_src = img_node.extract()[0]
                book['img'] = img_src
            else:
                print "cannot find book img"
            #extract introduction
            intro_nodes = hxs.xpath('//span[@class="all hidden"]/div/div[@class="intro"]/p/text()')
            if intro_nodes:
                book['intro'] = [i.extract() for i in intro_nodes]
            else:
                print "intro nodes not found"
            #extract content list
            content_list_xpath = '//h2/span[contains(text(),'+u'"目录")]/../following-sibling::*[@class="indent" and @style="display:none"]/text()'
            content_nodes = hxs.xpath(content_list_xpath)
            if content_nodes:
                book['content_list'] = [i.extract() for i in content_nodes]
            #pprint(book)
            yield book
        except Exception,e:
            print 'Exception Happened'
            print e
            raise


    def extract_info(self, line):
        if not line:
            return "",""
        line = string.strip(line)
        if not line:
            return "",""

        pos = string.index(line,':')
        if not pos or pos<0:
            return "",""
        field = line[:pos]
        #print "Field: "+field
        value = line[pos+2:]
        #print "Value: "+value
        return field,value
#end

