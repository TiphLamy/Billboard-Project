# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ArticleItem(scrapy.Item):
    album = scrapy.Field()
    artist = scrapy.Field()
    rank = scrapy.Field()
    peak=scrapy.Field()
    duration=scrapy.Field()
    last_week=scrapy.Field()

class NewscrawlerItem(scrapy.Item):

    pass


