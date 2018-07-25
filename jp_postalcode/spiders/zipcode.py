# -*- coding: utf-8 -*-
import scrapy
# from scrapy import Request

import sys
# sys.path.append('../../')

import copy
from time import sleep

from ..items import JpPostalcodeItem


class ZipcodeSpider(scrapy.Spider):
    name = 'zipcode'
    allowed_domains = ['www.zipcode-jp.com']
    start_urls = ['http://www.zipcode-jp.com/modules/zipcode/']

    def parse(self, response):

        # if not response.select('//get/site/logo'):
        #     yield Request(url=response.url, dont_filter=True)

        print("parse ken")
        # parent = response.xpath('//div[@id=\"contents\"]/p[1]/strong/text()').extract()
        # print('parent is:' + str(parent))

        total_count = response.xpath('//div[@id=\"contents\"]/p[2]/strong/text()').extract()
        print('total_count is:' + str(total_count))

        for sel in response.xpath('//tr[@class=\"even\"] | //tr[@class=\"odd\"]'):

            item = JpPostalcodeItem()
            item['ken'] = sel.xpath('td[1]/a/text()').extract()
            item['ken_jp'] = sel.xpath('td[2]/text() | td[2]/a/text()').extract()
            child_url_path = sel.xpath('td[1]/a/@href').extract()

            print('ken is:' + str(item['ken']))

            if item['ken']:
                if child_url_path:
                    # paging
                    # http://www.zipcode-jp.com/modules/zipcode/getarea.php?aid=13112&show=30&orderby=zidA&start=0
                    show = 30
                    for start in range(0, 120, 30):  # max num assumed to be 120
                        child_url = self.start_urls[0] + child_url_path[0] + \
                                    '&show=' + str(show) + '&start=' + str(start) + '&orderby=zid'

                        print("child url: " + child_url)
                        request = scrapy.Request(child_url, callback=self.parse_city)
                        request.meta['item'] = item
                        yield request
                else:
                    yield item

    def parse_city(self, response):
        print("parse city")
        total_count = response.xpath('//div[@id=\"contents\"]/p[2]/strong/text()').extract()
        print('total_count is:' + str(total_count))

        for sel in response.xpath('//tr[@class=\"even\"] | //tr[@class=\"odd\"]'):

            item = copy.deepcopy(response.meta['item'])
            item['city'] = sel.xpath('td[1]/a/text()').extract()
            item['city_jp'] = sel.xpath('td[2]/text() | td[2]/a/text()').extract()
            child_url_path = sel.xpath('td[1]/a/@href').extract()

            if item['city']:
                if child_url_path:
                    show = 30
                    for start in range(0, 120, 30):  # max num assumed to be 120
                        child_url = self.start_urls[0] + child_url_path[0] + \
                                    '&show=' + str(show) + '&start=' + str(start) + '&orderby=zid'

                        print("child url: " + child_url)
                        request = scrapy.Request(child_url, callback=self.parse_area)
                        request.meta['item'] = item
                        yield request
                else:
                    yield item

    def parse_area(self, response):
        print("parse area")
        total_count = response.xpath('//div[@id=\"contents\"]/p[2]/strong/text()').extract()
        print('total_count is:' + str(total_count))

        for sel in response.xpath('//tr[@class=\"even\"] | //tr[@class=\"odd\"]'):

            item = copy.deepcopy(response.meta['item'])
            item['zipcode'] = sel.xpath('td[1]/a/strong/text()').extract()
            item['area'] = sel.xpath('td[2]/text()').extract()
            item['area_jp'] = sel.xpath('td[3]/text() | td[3]/a/text()').extract()

            print("str(item['area']), str(item['area_jp']), str(item['zipcode'])\n")
            print(str(item['area']), str(item['area_jp']), str(item['zipcode']))
            if item['area']:
                yield item

"""
Refer links:
http://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/spiders.html

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class MySpider(CrawlSpider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com']

    rules = (
        # 提取匹配 'category.php' (但不匹配 'subsection.php') 的链接并跟进链接(没有callback意味着follow默认为True)
        Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # 提取匹配 'item.php' 的链接并使用spider的parse_item方法进行分析
        Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
    )

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url)

        item = scrapy.Item()
        item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
        item['name'] = response.xpath('//td[@id="item_name"]/text()').extract()
        item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
        return item
        
"""