# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import logging
import os
import sqlite3

from .spiders.books_douban_spider import BooksDoubanSpider
from .spiders.comments_douban_spider import CommentsDoubanSpider

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler('log_books_douban.txt')
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class BooksDoubanPipeline(object):
    def __init__(self):
        self.info = []
        self.comment_urls = []
        self.comments = []

    def process_item(self, item, spider):
        if isinstance(spider, BooksDoubanSpider):
            self.info.append(dict(item))
            self.comment_urls.append(item['comments'])

        if isinstance(spider, CommentsDoubanSpider):
            self.comments.append(dict(item))

        return item

    def close_spider(self, spider):
        if isinstance(spider, BooksDoubanSpider):
            with open('book_info.json', 'w', encoding='utf-8') as f_info:
                json.dump(self.info, f_info, indent=4,
                          separators=(',', ': '), ensure_ascii=False)

            with open('comment_urls.txt', 'w', encoding='utf-8') as f_urls:
                for url in self.comment_urls:
                    f_urls.write(url + '\n')

        if isinstance(spider, CommentsDoubanSpider):
            with open('book_comments.json', 'w', encoding='utf-8') as f_comments:
                json.dump(self.comments, f_comments, indent=4,
                          separators=(',', ': '), ensure_ascii=False)


class BooksDoubanDBPipeline(object):
    def __init__(self):
        self.info_cnt = 1
        self.comments_cnt = 1
        self.conn = sqlite3.connect('books_douban.db')
        self.db = self.conn.cursor()
        self.db.execute('''
                        CREATE TABLE IF NOT EXISTS book_info (
                        book_id          INT    PRIMARY KEY    NOT NULL,
                        title            TEXT                  NOT NULL,
                        author           TEXT                          ,
                        press            TEXT                          ,
                        producer         TEXT                          ,
                        subtitle         TEXT                          ,
                        original_name    TEXT                          ,
                        translator       TEXT                          ,
                        publish_date     TEXT                          ,
                        pages            INT                           ,
                        price            REAL                          ,
                        binding          TEXT                          ,
                        series           TXET                          ,
                        isbn             INT                           ,
                        avg_rating       REAL                          ,
                        comments_url     TEXT                          ,
                        comments_crawled INT                           ,
                        UNIQUE(book_id)                                );
                        ''')

        self.db.execute('''
                        CREATE TABLE IF NOT EXISTS book_comments (
                        record_id        INTEGER    PRIMARY KEY    AUTOINCREMENT,
                        book_id          INT                            NOT NULL,
                        title            TEXT                           NOT NULL,
                        rating           INT                            NOT NULL,
                        comment          TEXT                                  );
                        ''')

        self.conn.commit()

    def process_item(self, item, spider):
        if isinstance(spider, BooksDoubanSpider):
            self.db.execute('''
                            INSERT OR IGNORE INTO book_info (book_id, title,\
                            author, press, producer, subtitle, original_name,\
                            translator, publish_date, pages, price, binding,\
                            series, isbn, avg_rating, comments_url, comments_crawled)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                            ''',
                            (item['book_id'], item['title'], item['author'], item['press'],
                             item['producer'], item['subtitle'], item['original_name'],
                             item['translator'], item['publish_date'], item['pages'], item['price'],
                             item['binding'], item['series'], item['isbn'], item['avg_rating'],
                             item['comments_url'], item['comments_crawled'])
                            )
            if self.info_cnt % 200 == 0:
                self.conn.commit()
                logger.info(
                    '{} records inserted into book_info'.format(self.info_cnt))

            self.info_cnt += 1

        if isinstance(spider, CommentsDoubanSpider):
            self.db.execute('''
                            INSERT INTO book_comments (book_id, title,\
                            rating, comment) VALUES (?, ?, ?, ?);
                            ''',
                            (item['book_id'], item['title'],
                             item['rating'], item['comment'])
                            )
            if self.comments_cnt % 1000 == 0:
                self.conn.commit()
                logger.info('{} records inserted into book_comments'.format(
                    self.comments_cnt))

            self.comments_cnt += 1

        return item

    def close_spider(self, spider):
        if isinstance(spider, BooksDoubanSpider):
            logger.info('Crawling book_info complete. {} records in total.'.format(
                self.info_cnt - 1))

        if isinstance(spider, CommentsDoubanSpider):
            logger.info('Crawling book_comments complete. {} records in total.'.format(
                self.comments_cnt - 1))

        self.conn.commit()
        self.conn.close()
