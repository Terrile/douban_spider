#coding=UTF-8
import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
import re
import math
import urllib
from ..items import ProductItem #this is the way to import code from parent directory
from ..items import QuestionAnswerItem
import os
#set default encoding
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class jdscrapy(scrapy.Spider):
    name = "jdspider"
    allowed_domains = ["jd.com"]
    start_urls = [
        "http://list.jd.com/list.html?cat=737,794,798"
        #"http://club.jd.com/allconsultations/1258277-2-2.html"
    ]

    def parse(self, response):
        html_txt = response.body.decode("utf-8","ignore")
        hxs = Selector(text=html_txt)
        try:
            #products = hxs.select('//div[@class="lh-wrap"]/div[@class="p-name"]/a/@href')
            products = hxs.xpath('//div[@class="lh-wrap"]')

            for product in products:
                p_name = product.xpath('.//div[@class="p-name"]/a/text()')
                p_url = product.xpath('.//div[@class="p-name"]/a/@href')
                p_img = product.xpath('.//div[@class="p-img"]/a/img/@data-lazyload')
                p_price = product.xpath('.//div[@class="p-price"]/strong')
                item = ProductItem()
                item['p_title'] = p_name.extract()[0]
                item['p_url'] = p_url.extract()[0]
                item['p_img'] = p_img.extract()[0]
                m = re.search("[^\d]+(\d+)\.html",item['p_url'])
                if m:
                    p_id = m.groups()[0]
                    qa_url = "http://club.jd.com/allconsultations/"+p_id+"-2-1.html"
                    yield Request(url=qa_url,callback=self.parse_question_answer)
        except:
            pass

    #def parse_question_answer(self, response):
    def parse_question_answer(self, response):
            #html_txt = response.body.decode("utf-8","ignore")
            #html_txt = response.body.decode("utf-8","ignore")
            #hxs = Selector(text=html_txt)
            hxs = Selector(response)
            try:
                prod_info = hxs.xpath('//div[@class="mc"]/div[@class="p-name"]/a/@href')
                prod_url = prod_info.extract()[0]
                consults = hxs.xpath('//div[@class="Refer_List"]/div[@class="refer"]')
                for consult in consults:
                    ask = consult.xpath('.//dl[@class="ask"]/dd/a/text()')
                    answer = consult.xpath('.//dl[@class="answer"]/dd/text()')
                    item = QuestionAnswerItem()
                    item['p_url'] = prod_url

                    ask_str = ask.extract()[0].strip('\r\n\t')
                    ask_str = re.sub(r'\s+',' ',ask_str)
                    item['question'] = ask_str

                    answer_str = answer.extract()[0].strip('\r\n\t')
                    answer_str = re.sub(r'\s+',' ',answer_str)
                    item['answer'] = answer_str

                    yield item

                next_page = hxs.xpath('//div[@class="Pagination"]/a[@class="next"]/@href')
                next_page_url = next_page.extract()[0]
                yield Request(url=next_page_url,callback=self.parse_question_answer)
            except:
                pass