from celery import Celery
import os
from scrapy.crawler import CrawlerRunner
from get_prices_scrapy.spiders.cstoredecisions import CstoredecisionsSpider

app = Celery('tasks', broker=os.getenv('CELERY_BROKER', 'pyamqp://guest@localhost//'))

@app.task
def start_parsing():
    runner = CrawlerRunner()
    runner.crawl(CstoredecisionsSpider)