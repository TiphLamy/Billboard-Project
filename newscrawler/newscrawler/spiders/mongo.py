from pymongo import MongoClient


class MongoPipeline(object):

    collection_name = 'scrapy_items'


    def open_spider(self, spider):
        self.client = pymongo.MongoClient() #par défaut, paramétré sur localhost port 27017
        self.db = self.client["billboard"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        #self.db[self.collection_name].insert_one(dict(item))
        self.db[self.collection_name].insert_one(dict(item))
        #print("collection KIRK: " + str(self.db[self.collection_name].find_one({"album":"KIRK"})))
        #print("collection gospel: " + str(self.db[self.collection_name].find_one({"album":"Ghetto Gospel"})))

        #db_music = client.series
        #collection_billboard = db_music['billboard']
        #collection_billboard.insert_one({"album" :album,"artist":artist, "rank":rank})

        return item
