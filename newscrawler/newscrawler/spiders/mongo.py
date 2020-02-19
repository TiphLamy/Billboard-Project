from pymongo import MongoClient


class MongoPipeline(object):

    collection_name = 'scrapy_items'


    def open_spider(self, spider):
        self.client = pymongo.MongoClient() #par défaut, paramétré sur localhost port 27017
        self.db = self.client["billboard"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item
