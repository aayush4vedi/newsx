# -*- coding: utf-8 -*-
from urllib.parse import urlparse

import datetime
import pymysql
import pytz
import scrapy
from scrapy.crawler import CrawlerProcess
from dateutil.parser import parse
from env import HOST, DATABASE, USER, PASSWORD
from utils import find_my_domain


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
            # description = data.css('description::text').get('').strip()
            link = data.css('link::text').get().strip()

            tags = data.css('category::text').extract()
            tags = [t.lower() for t in tags]
            tags = ','.join(tags)
            domains = find_my_domain(tags) + find_my_domain(title) 
            domains = list(dict.fromkeys(domains))
            domains = ','.join(domains)
            item = {
                'link': response.urljoin(link),
                'title': title,
                # https://www.aljazeera.com/xml/rss/all.xml becomes aljazeera.com
                'source': '.'.join(parsed_uri.netloc.split('.')[-2:]),
                # convert datetime to UTC datetime
                'published_date': parse(data.css('pubDate::text').get()).astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S'),
                'tags': tags,
                'domains' : domains
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
            # print('Item: {} inserted to {}'.format(item, table))
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
            tags = [t.lower() for t in tags]
            tags = ','.join(tags)
            domains = find_my_domain(tags) + find_my_domain(title)
            domains = list(dict.fromkeys(domains))
            domains = ','.join(domains)
            item = {
                'link': response.urljoin(link),
                'title': title,
                # https://www.aljazeera.com/xml/rss/all.xml becomes aljazeera.com
                'source': '.'.join(parsed_uri.netloc.split('.')[-2:]),
                # convert datetime to UTC datetime
                'published_date': parse(data.css('published::text').get()).astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S'),
                'tags': tags,
                'domains' : domains
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
            # print('Item: {} inserted to {}'.format(item, table))
        except Exception as e:
            print('Error {} while inserting {}'.format(e, item))
            return False

class RssScraperSpiderProductHunt(scrapy.Spider):
    name = 'rss_scraper_producthunt'

    conn = pymysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    
    start_urls = [
        'https://www.producthunt.com/feed'
    ]

    def parse(self, response):
        parsed_uri = urlparse(response.url)
        print("\n\t\t ==> Running for URL#2: {}".format(parsed_uri.netloc))
        response.selector.remove_namespaces()
        for data in response.css('entry'):
            title = data.css('title::text').get('').strip()
            # description = data.css('content::text').get('').strip()
            link = data.css('link').xpath("@href").extract()

            tags = 'product_hunt'       # As PH's Rss doesnt give tags
            domains = find_my_domain(tags) + find_my_domain(title) 
            domains = list(dict.fromkeys(domains))
            domains = ','.join(domains)
            item = {
                'link': link,
                'title': title,
                'source': '.'.join(parsed_uri.netloc.split('.')[-2:]),
                'published_date': parse(data.css('published::text').get()).astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S'),
                'tags': tags,
                'domains' : domains
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
            # print('Item: {} inserted to {}'.format(item, table))
        except Exception as e:
            print('Error {} while inserting {}'.format(e, item))
            return False


class RssScraperSpiderReddit(scrapy.Spider):
    name = 'rss_scraper_reddit'

    conn = pymysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    
    subreddit_list = [
        'compsci',
        'computerscience',
        'distributed',
        'datastructures',
        'algorithms',
        'cpp_questions',
        'GAMETHEORY',
        'Discretemathematics',
        'crypto',
        'cryptography',
        'logic',
        'computerarchitecture',
        'compilers',
        'Network',
        'ReverseEngineering',
        'osdev',
        'Android',
        'MacOS',
        'osx',
        'windows',
        'linux',
        'kernel',
        'linuxdev',
        'linuxquestions',
        'Ubuntu',
        'hacking',
        'HowToHack',
        'Hacking_Tutorials',
        'hackers',
        'robotics',
        'arduino',
        'virtualreality',
        'augmentedreality',
        'IOT',
        'computervision',
        'opencv',
        'imageprocessing',
        'dip',
        'datamining',
        'textdatamining',
        'MachineLearning',
        'learnmachinelearning',
        'ResearchML',
        'neuralnetworks',
        'neuralnetworks',
        'NeuralNetwork',
        'deeplearning',
        'DeepLearningPapers',
        'deeplearners',
        'datascience',
        'learndatascience',
        'Database',
        'datasets',
        'statistics',
        'AskStatistics',
        'Rlanguage',
        'rstats',
        'matlab',
        'scala',
        'scikit_learn',
        'JupyterNotebooks',
        'kaggle',
        'datacleaning',
        'NLP',
        'LanguageTechnology',
        'bigdata',
        'apachespark',
        'hadoop',
        'visualization',
        'dataisbeautiful',
        'tableau',
        'excel',
        'ExcelTips',
        'artificial',
        'ArtificialInteligence',
        'softwaredevelopment',
        'programming',
        'coding',
        'SoftwareEngineering',
        'ProgrammingLanguages',
        'learnprogramming',
        'functionalprogramming',
        'asm',
        'C_Programming',
        'c_language',
        'cpp',
        'Cplusplus',
        'Python',
        'scala',
        'erlang',
        'haskell',
        'java',
        'javascript',
        'lisp',
        'perl',
        'PHP',
        'ruby',
        'rust',
        'dotnet',
        'Kotlin',
        'html',
        'html',
        'css',
        'rails',
        'django',
        'reactjs',
        'git',
        'github',
        'gitlab',
        'virtualization',
        'browsers',
        'aws',
        'AWS_cloud',
        'AZURE',
        'azuredevops',
        'kubernetes',
        'k8s',
        'docker',
        'GCP',
        'vim',
        'neovim',
        'vim_magic',
        'emacs',
        'appdev',
        'AppDevelopment',
        'iosdev',
        'iOSProgramming',
        'androiddev',
        'devops',
        'netsec',
        'compsec',
        'websec',
        'computergraphics',
        'web_design',
        'UI_Design',
        'UI_programming',
        'UXDesign',
        'UXResearch',
        'UX_Design',
        'webdev',
        'softwaretesting',
        'systems',
        'tinycode',
        'api',
        'gamedev',
        'programmingchallenges',
        'opensource',
        'AskComputerScience',
        'forhire',
        'cscareerquestions',
        'interviewpreparations',
        'csinterviewproblems',
        'interviews',
        'technology',
        'TrueReddit',
        'wikipedia',
        'geek',
        'skeptic',
        'blog',
        'COPYRIGHT',
        'noip',
        'cognitivescience',
        'torrents',
        'books',
        'scifi',
        'bookclub',
        'writing',
        'atheism',
        'philosophy',
        'history',
        'AskHistorians',
        'business',
        'Flipping',
        'freelance',
        'Upwork',
        'SaaS',
        'SideProject',
        'marketing',
        'SEO',
        'bigseo',
        'SEO_Digital_Marketing',
        'science',
        'askscience',
        'AskPhysics',
        'chemistry',
        'biology',
        'medicine',
        'neuroscience',
        'geology',
        'environment',
        'Health',
        'Physics',
        'space',
        'aerospace',
        'quantum',
        'QuantumPhysics',
        'energy',
        'FluidMechanics',
        'engineering',
        'electronics',
        'ECE',
        'ElectricalEngineering',
        'AskEngineers',
        'LearnEngineering',
        'AskElectronics',
        'MechanicalEngineering',
        'EngineeringStudents',
        'rocketry',
        'aviation',
        'nasa',
        'spacex',
        'aerodynamics',
        'StructuralEngineering',
        '3Dprinting',
        'math',
        'mathematics',
        'calculus',
        'DifferentialEquations',
        'Algebra',
        'GraphTheory',
        'Economics',
        'economy',
        'finance',
        'personalfinance',
        'Accounting',
        'invest',
        'invest',
        'BlockchainStartups',
        'CryptoCurrency',
        'Bitcoin',
        'BitcoinBeginners',
        'bitcointrading',
        'BitcoinDiscussion'
    ]

    start_urls = ['http://www.reddit.com/r/' + subreddit + '/.rss' for subreddit in subreddit_list]

    def parse(self, response):
        parsed_uri = urlparse(response.url)
        print("\n\t\t ==> Running for URL#3: {}".format(parsed_uri.netloc + parsed_uri.path))
        response.selector.remove_namespaces()
        for data in response.css('entry'):
            title = data.css('title::text').get('').strip()
            # description = data.css('content::text').get('').strip()
            link = data.css('link').xpath("@href").extract()

            tags = data.css('category').xpath("@term").extract()
            tags = [t.lower() for t in tags]
            tags = ','.join(tags)
            domains = find_my_domain(tags)
            domains = ','.join(domains)
            item = {
                'link': link,
                'title': title,
                'source': '.'.join(parsed_uri.netloc.split('.')[-2:]),
                'published_date': parse(data.css('updated::text').get()).astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S'),
                'tags': tags,
                'domains' : domains
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
            # print('Item: {} inserted to {}'.format(item, table))
        except Exception as e:
            print('Error {} while inserting {}'.format(e, item))
            return False


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(RssScraperSpiderGeneric)
    process.crawl(RssScraperSpiderStackoverflow)
    process.crawl(RssScraperSpiderProductHunt)
    process.crawl(RssScraperSpiderReddit)
    process.start() # the script will block here until the crawling is finished
    print("\n\n ********************************************************** Ran Spiders at: {}\n\n".format(datetime.datetime.now()))


## Create table in db

'''
* create database cynical_reader
* use cynical_reader;
* create table:

drop table data;
CREATE TABLE `data` (
  `link` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `source` varchar(255) DEFAULT NULL,
  `published_date` varchar(255) DEFAULT NULL,
  `tags` varchar(9999) DEFAULT NULL,
  `domains` varchar(999) DEFAULT NULL
);
CREATE UNIQUE INDEX uniq_idx
ON cynical_reader.data(source,title,published_date);


25 * * * * /usr/local/bin/python3 /Users/aayush.chaturvedi/Sandbox/mc_cn/rss_scraper.py >> /Users/aayush.chaturvedi/Sandbox/mc_cn/cron_logs.txt 2>&1                            

'''


