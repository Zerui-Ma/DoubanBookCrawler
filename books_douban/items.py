# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    book_id = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    press = scrapy.Field()
    producer = scrapy.Field()
    subtitle = scrapy.Field()
    original_name = scrapy.Field()
    translator = scrapy.Field()
    publish_date = scrapy.Field()
    pages = scrapy.Field()
    price = scrapy.Field()
    binding = scrapy.Field()
    series = scrapy.Field()
    isbn = scrapy.Field()
    avg_rating = scrapy.Field()
    comments_url = scrapy.Field()
    comments_crawled = scrapy.Field()

class BookCommentsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    book_id = scrapy.Field()
    title = scrapy.Field()
    rating = scrapy.Field()
    comment = scrapy.Field()
