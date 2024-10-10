# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SrcSjtuItem(scrapy.Item):
    # define the fields for your item here like:
    date = scrapy.Field()
    title = scrapy.Field()
    rank = scrapy.Field()
    author = scrapy.Field()
    authorRank = scrapy.Field()
    grade = scrapy.Field()
    tnum = scrapy.Field()
    bnum = scrapy.Field()
    team = scrapy.Field()
    pass
