# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy import signals
import json
import codecs
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
import MySQLdb
import MySQLdb.cursors

class MyImagesPipeline(ImagesPipeline):
    DIR_PATH='E:/Test/src/demo/static/full/%s'
    def file_path(self, request, response=None, info=None):
        global DIR_PATH
        image_guid = request.url.split('/')[-1]
        return 'E:/Test/src/demo/static/pic/%s' % (image_guid)

        
class JsonWithEncodingLinkedinPipeline(object):
    def __init__(self):
        self.file = codecs.open('linkedin.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
    def spider_closed(self, spider):
        self.file.close()
