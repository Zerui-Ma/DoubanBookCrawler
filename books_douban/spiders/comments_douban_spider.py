#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# author: mazr

import os
import re
import sqlite3

import scrapy

from ..items import BookCommentsItem


class CommentsDoubanSpider(scrapy.Spider):
    name = "comments_douban"
    conn = sqlite3.connect('books_douban.db')
    db = conn.cursor()
    try:
        records = db.execute('''
                            SELECT comments_url FROM book_info
                            WHERE comments_crawled = 0;
                            ''').fetchall()
        db.execute('''
                UPDATE book_info SET comments_crawled = 1;
                ''')
        conn.commit()
        start_urls = [r[0] for r in records if r[0].strip()]

    except Exception:
        pass


    def parse(self, response):
        title = response.xpath(
            '//div[@id="content"]/h1/text()').extract_first()
        title = ' '.join(title.split()[:-1])
        for comment in response.xpath('//div[@class="comment"]'):
            rating = comment.xpath('.//span[@title]/@title').extract_first()
            if rating:
                if rating == '力荐':
                    rating = 5
                elif rating == '推荐':
                    rating = 4
                elif rating == '还行':
                    rating = 3
                elif rating == '较差':
                    rating = 2
                elif rating == '很差':
                    rating = 1

                short = comment.xpath(
                    './/span[@class="short"]/text()').extract_first()
                book_id = response.url.split('/')[4]
                yield BookCommentsItem({'book_id': book_id, 'title': title, 'rating': rating, 'comment': short})

        next_page = response.xpath(
            '//ul[@class="comment-paginator"]/li[3]/a/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
