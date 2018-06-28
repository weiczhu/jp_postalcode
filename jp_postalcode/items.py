# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JpPostalcodeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass

    ken = scrapy.Field()
    ken_jp = scrapy.Field()
    city = scrapy.Field()
    city_jp = scrapy.Field()
    area = scrapy.Field()
    area_jp = scrapy.Field()
    zipcode = scrapy.Field()

