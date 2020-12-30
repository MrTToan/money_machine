# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VietstockItem(scrapy.Item):
    date = scrapy.Field()
    time = scrapy.Field()
    stock_name = scrapy.Field()
    price = scrapy.Field()

