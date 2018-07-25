# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.exceptions import DropItem

class JpPostalcodePipeline(object):

    def __init__(self):
        self.file = open('data/items.jl', 'wb')
        self.ids_seen = set()

    def process_item(self, item, spider):
        # if item['price']:
        #     if item['price_excludes_vat']:
        #         item['price'] = item['price'] * self.vat_factor
        #     return item
        # else:
        #     raise DropItem("Missing price in %s" % item)

        line = json.dumps(dict(item)) + "\n"
        self.file.write(line.encode(encoding='utf-8'))

        # if item['id'] in self.ids_seen:
        #     raise DropItem("Duplicate item found: %s" % item)
        # else:
        #     self.ids_seen.add(item['id'])
        #     return item
