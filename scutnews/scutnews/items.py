# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ScutnewsItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    publish_time = scrapy.Field()
    submit_time = scrapy.Field()
    department = scrapy.Field()
    view_count = scrapy.Field()
    img_url = scrapy.Field()
    content = scrapy.Field()
    last_modified = scrapy.Field