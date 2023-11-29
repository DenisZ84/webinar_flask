import time
import random

from celery import Celery
import os
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from get_prices_scrapy import settings as scraper_settings


app = Celery('tasks', broker=os.getenv('CELERY_BROKER', 'pyamqp://guest@localhost//'))

@app.task(name='getPrices')
def start_parsing():
    crawler_settings = Settings()
    crawler_settings.setmodule(scraper_settings)
    runner = CrawlerRunner(settings=crawler_settings)
    runner.crawl("cstoredecisions")


@app.task(name='addTask')  # Named task
def add(x, y):
    print('Task Add started')
    time.sleep(10 * random.random())  # Simulate a long task
    print('Task Add done')
    return x + y