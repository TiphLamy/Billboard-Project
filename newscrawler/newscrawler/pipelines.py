# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from pymongo import MongoClient

class NewscrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class TextPipeline(object):

    def clean_spaces(self,string):
        if string:
        	return " ".join(string.split())

    def process_item(self, item, spider):
        if item['album']:
            item["album"] = self.clean_spaces(item["album"])
            item["artist"] = self.clean_spaces(item["artist"])
            return item
        else:
            raise DropItem("Missing title in %s" % item)



class MongoPipeline(object):

    collection_name = 'billboard'

    def open_spider(self, spider):
        self.client = MongoClient() #par défaut, paramétré sur localhost port 27017
        self.db = self.client["client_name"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db['billboard'].insert_one(dict(item))

        return item
