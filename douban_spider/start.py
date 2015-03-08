# -*- coding: utf-8 -*-
from scrapy import cmdline
__author__ = 'Min'

if __name__ == "__main__":
    print "Hello World"
    cmdline.execute("scrapy crawl bookspider".split())