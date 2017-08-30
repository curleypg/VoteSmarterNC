# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NclegItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Member(scrapy.Item):
    member = scrapy.Field()
    href = scrapy.Field()
