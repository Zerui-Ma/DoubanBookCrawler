# DoubanBookCrawler

## 该Scrapy项目可用于爬取豆瓣网上特定类别的书籍信息和书评并存入数据库

## 使用步骤：

### 1. 替换`DoubanBookCrawler\books_douban\spiders\books_douban_spider.py`中的`start_urls`变量指定爬取的书籍类别

### 2. 运行`scrapy crawl books_douban`爬取书籍信息并存入根目录下`books_douban.db`的`book_info`表中

### 3. 运行`scrapy crawl comments_douban`爬取已入库书籍的书评并存入根目录下`books_douban.db`的`book_comments`表中
