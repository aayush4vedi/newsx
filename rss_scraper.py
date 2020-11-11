# -*- coding: utf-8 -*-
from urllib.parse import urlparse

import pymysql
import pytz
import scrapy
from scrapy.crawler import CrawlerProcess
from dateutil.parser import parse
from env import HOST, DATABASE, USER, PASSWORD


class RssScraperSpiderGeneric(scrapy.Spider):
    '''
        for rss feed in same xml format at start_urls
    '''
    name = 'rss_scraper_generic'

    conn = pymysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    
    start_urls = [
        'https://hackernoon.com/feed',
        'https://dev.to/feed/',
        'https://lobste.rs/rss',
    ]

    def parse(self, response):
        parsed_uri = urlparse(response.url)
        print("\n\t\t ----------------> Running for URL: {}".format(parsed_uri.netloc))
        for data in response.css('item'):
            title = data.css('title::text').get('').strip()
            description = data.css('description::text').get('').strip()
            link = data.css('link::text').get().strip()

            tags = data.css('category::text').extract()
            item = {
                'link': response.urljoin(link),
                'title': title,
                # https://www.aljazeera.com/xml/rss/all.xml becomes aljazeera.com
                'source': '.'.join(parsed_uri.netloc.split('.')[-2:]),
                # convert datetime to UTC datetime
                'published_date': parse(data.css('pubDate::text').get()).astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S'),
                'tags': ','.join(tags)
            }
            self.insert_into_db('data', item)
        print ("\n\n************************* Scrapy done all right ***********************\n\n")

    def insert_into_db(self, table, item, key=None):
        try:
            placeholder = ', '.join(["%s"] * len(item))
            statement = 'INSERT IGNORE INTO {table} ({columns}) VALUES ({values})'.format(
                table=table, columns=','.join(item.keys()), values=placeholder)
            self.cursor.execute(statement, list(item.values()))
            self.conn.commit()
            print('Item: {} inserted to {}'.format(item, table))
        except Exception as e:
            print('Error {} while inserting {}'.format(e, item))
            return False

class RssScraperSpiderStackoverflow(scrapy.Spider):
    name = 'rss_scraper_stackoverflow'

    conn = pymysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    
    start_urls = [
        'https://stackoverflow.com/feeds?sort=newest'
        # 'https://mshibanami.github.io/GitHubTrendingRSS/daily/all.xml'  TODO: 1
        # 'https://news.ycombinator.com/rss', #TODO: 2
    ]

    def parse(self, response):
        parsed_uri = urlparse(response.url)
        print("\n\t\t ==> Running for URL#2: {}".format(parsed_uri.netloc))
        response.selector.remove_namespaces()
        for data in response.css('entry'):
            title = data.css('title::text').get('').strip()
            description = data.css('summary::text').get('').strip()
            link = data.css('uri::text').get().strip()

            tags = data.css('category').xpath("@term").extract()
            item = {
                'link': response.urljoin(link),
                'title': title,
                # https://www.aljazeera.com/xml/rss/all.xml becomes aljazeera.com
                'source': '.'.join(parsed_uri.netloc.split('.')[-2:]),
                # convert datetime to UTC datetime
                'published_date': parse(data.css('published::text').get()).astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S'),
                'tags': ','.join(tags)
            }
            self.insert_into_db('data', item)
        print ("\n\n************************* Scrapy done all right ***********************\n\n")

    def insert_into_db(self, table, item, key=None):
        try:
            placeholder = ', '.join(["%s"] * len(item))
            statement = 'INSERT IGNORE INTO {table} ({columns}) VALUES ({values})'.format(
                table=table, columns=','.join(item.keys()), values=placeholder)
            self.cursor.execute(statement, list(item.values()))
            self.conn.commit()
            print('Item: {} inserted to {}'.format(item, table))
        except Exception as e:
            print('Error {} while inserting {}'.format(e, item))
            return False


class RssScraperSpiderReddit(scrapy.Spider):
    name = 'rss_scraper_reddit'

    conn = pymysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    
    start_urls = [
        
    ]

    def parse(self, response):
        parsed_uri = urlparse(response.url)
        print("\n\t\t ==> Running for URL#2: {}".format(parsed_uri.netloc))
        response.selector.remove_namespaces()
        for data in response.css('entry'):
            title = data.css('title::text').get('').strip()
            description = data.css('summary::text').get('').strip()
            link = data.css('uri::text').get().strip()

            tags = data.css('category').xpath("@term").extract()
            item = {
                'link': response.urljoin(link),
                'title': title,
                # https://www.aljazeera.com/xml/rss/all.xml becomes aljazeera.com
                'source': '.'.join(parsed_uri.netloc.split('.')[-2:]),
                # convert datetime to UTC datetime
                'published_date': parse(data.css('published::text').get()).astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S'),
                'tags': ','.join(tags)
            }
            self.insert_into_db('data', item)
        print ("\n\n************************* Scrapy done all right ***********************\n\n")

    def insert_into_db(self, table, item, key=None):
        try:
            placeholder = ', '.join(["%s"] * len(item))
            statement = 'INSERT IGNORE INTO {table} ({columns}) VALUES ({values})'.format(
                table=table, columns=','.join(item.keys()), values=placeholder)
            self.cursor.execute(statement, list(item.values()))
            self.conn.commit()
            print('Item: {} inserted to {}'.format(item, table))
        except Exception as e:
            print('Error {} while inserting {}'.format(e, item))
            return False


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(RssScraperSpiderGeneric)
    process.crawl(RssScraperSpiderStackoverflow)
    process.start() # the script will block here until the crawling is finished


## Create table in db

'''
* create database cynical_reader
* use cynical_reader;
* create table:

    CREATE TABLE `data` (
  `link` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `source` varchar(255) DEFAULT NULL,
  `published_date` varchar(255) DEFAULT NULL,
  `tags` varchar(9999) DEFAULT NULL
);

feed:nth-child(1) > entry:nth-child(8)
/feed/entry[1]

response.selector.register_namespace('namesp', 
                                     'http://www.w3.org/2005/Atom')

response.css('namesp:feed').get()                                     
response.xpath('/namesp:feed/entry').get()      

response.selector.remove_namespaces()
response.css('feed').get()                                     

'''