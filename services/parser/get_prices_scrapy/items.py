# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PricesItem(scrapy.Item):
    city_name = scrapy.Field()
    date = scrapy.Field()
    price = scrapy.Field()
