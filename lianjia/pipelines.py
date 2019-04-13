# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

import pymongo

from scrapy.conf import settings

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class LianjiaPipeline(object):
    def __init__(self):
        self.filename = open("lj.json", "w")

    def process_item(self, item, spider):
        # ensure_ascii=False禁用Ascii码，采用unicode码
        content = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.filename.write(content.encode("utf-8"))
        return item

    def close_spider(self, spider):
        self.filename.close()


