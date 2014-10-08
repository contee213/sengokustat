# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class BushoCard(scrapy.Item):
    """
    武将カード
    """
    heishu = scrapy.Field()
    buke = scrapy.Field()
    card_no = scrapy.Field()
    name = scrapy.Field()
    name_yomi = scrapy.Field()
    buryoku = scrapy.Field()
    tousotsu = scrapy.Field()
    rarity = scrapy.Field()
    tokugi = scrapy.Field()
    keiryaku = scrapy.Field()
    cost = scrapy.Field()