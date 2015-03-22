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
from scrapy import log
from ..items import Book #this is the way to import code from parent directory
from ..items import BookSnippet
import os
#set default encoding
import sys
import time
#import pprint
from pprint import pprint
reload(sys)
sys.setdefaultencoding('utf-8')

class BookSpider(scrapy.Spider):
    handle_httpstatus_list = [403,404]
    name = "bookspider"
    allowed_domains = ["douban.com"]
    start_urls = [
        #u'http://book.douban.com/tag/%E4%BA%92%E8%81%94%E7%BD%91?start=0&type=T'
        u'http://book.douban.com/tag/'
    ]

    def parse(self, response):
        try:
            log.msg('start to parse url: '+str(response.url))
            if response.status == 403:
                time.sleep(10)
                log.msg("MISSED URL: "+str(response.url),level=log.WARNING)
                pass
            html_txt = response.body.decode("utf-8","ignore")
            hxs = Selector(text=html_txt)
            items = hxs.xpath('//table/tbody/tr/td/a/@href')
            if items:
                for item in items:
                    tag = item.extract()
                    tag = tag[2:]
                    #tag = tag.encode('utf-8')
                    tag_url = 'http://book.douban.com/tag/'+tag+'?start=0&type=T'
                    log.msg('send out request for url: '+tag_url)
                    yield Request(url=tag_url,callback=self.parse_list)
            else:
                log.msg('no tag url found in start page',level=log.CRITICAL)
        except Exception,e:
            log.msg('failed to parse url: '+str(response.url))
            log.msg(str(e))
            raise

    def parse_list(self, response):
        try:
            if response.status == 403:
                time.sleep(10)
                log.msg("MISSED URL: "+str(response.url),level=log.WARNING)
                pass
            html_txt = response.body.decode("utf-8","ignore")
            url = response.url
            hxs = Selector(text=html_txt)
            #items = hxs.xpath('//ul[@class="subject-list"]/li[@class="subject-item"]/div/h2/a/@href')
            items = hxs.xpath('//ul[@class="subject-list"]/li[@class="subject-item"]')
            if items:
                for item in items:
                    snippet = BookSnippet()
                    pic = item.xpath('./div[@class="pic"]/a/@href')
                    if pic:
                        snippet['img']=pic.extract()[0]
                    title = item.xpath('./div[@class="info"]/h2/a')
                    if title:
                        link = title.xpath('./@href')
                        snippet['url'] = link.extract()[0]
                        title_txt = title.xpath('./text()')
                        snippet['title'] = title_txt.extract()[0]
                    pub = item.xpath('./div[@class="info"]/div[@class="pub"]/text()')
                    if pub:
                        snippet['pubinfo']=pub.extract()
                    rating = item.xpath('./*/span[@class="rating_nums"]/text()')
                    if rating:
                        snippet['rating'] = rating.extract()[0]
                    yield snippet
                    snippet_url = snippet['url']
                    if snippet_url:
                        log.msg('send request '+str(snippet_url))
                        yield Request(url=snippet_url,callback=self.parse_book)
                m = re.search(r'start=(\d+)',url)
                if m:
                    book_num = int(m.group(1)) + 20
                    log.msg('Book: '+ str(book_num)+' is processed',level=log.INFO)
                    next_page = u'http://book.douban.com/tag/%E4%BA%92%E8%81%94%E7%BD%91?start='+str(book_num)+u'&type=T'
                    if book_num<1000:
                        yield Request(url=next_page,callback=self.parse_list)
                else:
                    log.msg('Invalid url '+str(response.url),level=log.WARNING)
            else:
                log.msg('Not found items '+str(response.url),level=log.WARNING)
        except Exception,e:
            log.msg(str(e),level=log.WARNING)
            raise

    def parse_book(self, response):
        html_txt = response.body.decode("utf-8","ignore")
        hxs = Selector(text=html_txt)
        book = Book()
        try:
            if response.status == 403:
                time.sleep(60*5)
                log.msg("FAILURE 403 RESPONSE: "+str(response.url),level=log.ERROR);
                pass
            book_node = hxs.xpath('//div[@id="wrapper"]')
            title_node = book_node.xpath('.//h1/span/text()')
            info_node = book_node.xpath('.//div[@id="info"]')
            if not info_node:
                log.msg("FAILURE NO INFO NODE: "+str(response.url),level=log.ERROR);
                pass
            book['douban_url'] = response.url
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
                    book['release_year'] = value
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
            log.msg('SUCCEED BOOK: '+str(response.url),log.INFO)
            yield book
            self.parse_related_book(hxs)
            #start to extract related book here
        except Exception,e:
            print 'Exception Happened'
            print e
            raise

    def parse_related_book(self,selector):
        items = selector.xpath('//a/@href')
        if items:
            for item in items:
                book_url = item.extract()
                if re.match('http:\/\/book\.douban\.com\/subject\/\d+\/',book_url):
                    log.msg('RELATED BOOK: '+str(book_url))
                    yield Request(url=book_url,callback=self.parse_book)

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

