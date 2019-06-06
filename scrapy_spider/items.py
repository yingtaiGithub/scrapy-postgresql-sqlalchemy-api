# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    size_weight = scrapy.Field()
    price = scrapy.Field()
    unit = scrapy.Field()
    prices = scrapy.Field()
    price_min = scrapy.Field()
    price_avg = scrapy.Field()
