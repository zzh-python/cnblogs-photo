# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.exceptions import DropItem
class CnblogspiderPipeline(object):
    def __init__(self):
        self.file=open('papers.json','w+')  #用wb看不到，问题暂留
    def process_item(self, item, spider):
        if item['title']:
            line=json.dumps(dict(item))+ "\n"
            print('zzh:'+line)
            self.file.write(line)
            return item
        else:
            raise DropItem("Missing title in %s" % item)
