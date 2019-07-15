#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# author: mazr

import re

import scrapy

from ..items import BookInfoItem


def filter(string):
    return re.sub(r' |\n|:|：', '', string)


class BooksDoubanSpider(scrapy.Spider):
    name = "books_douban"
    offsets = range(0, 1000, 20)
    # 小说
    # start_urls = [
    #     'https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start={}&type=T'\
    #     .format(str(offset)) for offset in offsets
    # ]

    # 散文
    # start_urls = [
    #     'https://book.douban.com/tag/%E6%95%A3%E6%96%87?start={}&type=T'\
    #     .format(str(offset)) for offset in offsets
    # ]

    # 外国文学
    start_urls = [
        'https://book.douban.com/tag/%E5%A4%96%E5%9B%BD%E6%96%87%E5%AD%A6?start={}&type=T'\
        .format(str(offset)) for offset in offsets
    ]

    def parse(self, response):
        book_links = response.xpath('//a[@title]/@href').extract()
        for link in book_links:
            yield response.follow(link, self.parse_book)

    def parse_book(self, response):
        matching = {'作者': 'author', '出版社': 'press', '出品方': 'producer', '副标题': 'subtitle',\
                    '原作名': 'original_name', '译者': 'translator', '出版年': 'publish_date',\
                    '页数': 'pages', '定价': 'price', '装帧': 'binding', '丛书': 'series', 'ISBN': 'isbn'}

        info_dict = {'book_id': None, 'title': None, 'author': None, 'press': None, 'producer': None,\
                     'subtitle': None, 'original_name': None, 'translator': None, 'publish_date': None,\
                     'pages': None, 'price': None,'binding': None, 'series': None, 'isbn': None,\
                     'avg_rating': None, 'comments_url': None, 'comments_crawled': None}

        info_dict['title'] = \
            response.xpath('//span[@property="v:itemreviewed"]/text()').extract_first().strip()

        info_dict['avg_rating'] = \
            response.xpath('//strong/text()').extract_first().strip()

        book_id = response.url.split('/')[-2]
        info_dict['comments_url'] = 'https://book.douban.com/subject/{}/comments/'\
            .format(book_id)

        info_dict['book_id'] = book_id
        info_dict['comments_crawled'] = 0


        for item in response.xpath('//div[@id="info"]//span[@class="pl"]'):
            item_name = filter(item.xpath('./text()').extract_first())
            if item_name in ['作者', '出品方', '译者', '丛书']:
                info_dict[matching[item_name]] = \
                    filter(item.xpath('./following-sibling::*[1]/text()').extract_first())

            else:
                content = item.xpath('./following::text()[1]').extract_first().strip()
                if item_name == '定价':
                    content = re.findall(r'\d+.\d*', content)[0]

                info_dict[matching[item_name]] = content

        yield BookInfoItem(info_dict)
