# -*- coding: utf-8 -*-
import scrapy


class ZipcodeSpider(scrapy.Spider):
    name = 'zipcode'
    allowed_domains = ['http://www.zipcode-jp.com/modules/zipcode/']
    start_urls = ['http://http://www.zipcode-jp.com/modules/zipcode//']

    def parse(self, response):
        pass
