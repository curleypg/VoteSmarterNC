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

class Bill(scrapy.Item):
    number = scrapy.Field()
    chamber = scrapy.Field()
    session = scrapy.Field()
    session_id = scrapy.Field()
    title = scrapy.Field()
    counties = scrapy.Field()
    statutes = scrapy.Field()
    primary_sponsors = scrapy.Field()
    primary_sponsors_ids = scrapy.Field()
    sponsors = scrapy.Field()
    sponsors_ids = scrapy.Field()
    keywords = scrapy.Field()
    is_law  = scrapy.Field()
    is_ratified = scrapy.Field()
    is_vetoed = scrapy.Field()
    passed_House = scrapy.Field()
    passed_Senate = scrapy.Field()

class Member(scrapy.Item):
    chamber = scrapy.Field()
    district = scrapy.Field()
    href = scrapy.Field()
    member = scrapy.Field()
    memberId = scrapy.Field()
    party = scrapy.Field()
    email = scrapy.Field()

class MemberVotes(scrapy.Item):
    member = scrapy.Field()
    memberId = scrapy.Field()
    district = scrapy.Field()
    href = scrapy.Field()
    chamber = scrapy.Field()
    rcs = scrapy.Field()
    bill = scrapy.Field()
    billTitle = scrapy.Field()
    motion = scrapy.Field()
    date = scrapy.Field()
    vote = scrapy.Field()
    aye = scrapy.Field()
    nay = scrapy.Field()
    nv = scrapy.Field()
    excabs = scrapy.Field()
    excvote = scrapy.Field()
    totalvote = scrapy.Field()
    result = scrapy.Field()
    session = scrapy.Field()
