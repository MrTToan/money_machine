import scrapy
import time
from ..items import *
from scrapy.crawler import CrawlerProcess
from datetime import datetime, date, time
from bs4 import BeautifulSoup
import time as t


user_agent = 'Mozilla/5.0'
headers = {'User-Agent': user_agent }
class StockSpider(scrapy.Spider):
    name = "stock"
    urls = [
            'https://finance.vietstock.vn/MWG-ctcp-dau-tu-the-gioi-di-dong.htm',
            'https://finance.vietstock.vn/VNM-ctcp-sua-viet-nam.htm'
        ]

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        with open('index.html', 'wb') as f:
            f.write(soup.prettify().encode('utf-8'))
        price = soup.find_all("h2", class_="text-bold no-m-t r1")
        stock_name = soup.find_all("span", class_ = "h4 title")
        now = datetime.now()

        items = {
            'date': date.today(),
            'time': datetime.now(),
            'stock_name': stock_name[0].a.string,
            'price': float(price[0].span.string.replace(',', '.'))
        }

        stock = VietstockItem()
        stock['date'] = items['date']
        stock['time'] = items['time']
        stock['stock_name'] = items['stock_name']
        stock['price'] = items['price']
        yield stock


if __name__ == '__main__':
    ti = datetime.now()
    today = str(date.today())
    defined_time_string = today + ' 18:15:00'
    defined_time = datetime.strptime(defined_time_string, "%Y-%m-%d %H:%M:%S")
    process = CrawlerProcess()
    process.crawl(StockSpider)
    
    while ti <= defined_time:
        process.start()
        t.sleep(30)
        ti = datetime.now()


    

