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
    vote = scrapy.Field()

class MemberVotes(scrapy.Item):
    chamber = scrapy.Field()
    rcs = scrapy.Field()
    bill = scrapy.Field()
    motion = scrapy.Field()
    motiontwo = scrapy.Field()
    date = scrapy.Field()
    vote = scrapy.Field()
    aye = scrapy.Field()
    nay = scrapy.Field()
    nv = scrapy.Field()
    excabs = scrapy.Field()
    excvote = scrapy.Field()
    totalvote = scrapy.Field()
    result = scrapy.Field()
