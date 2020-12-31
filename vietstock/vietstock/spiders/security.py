import scrapy
import time
from ..items import *
from scrapy.crawler import CrawlerProcess
from datetime import datetime, date, time
from bs4 import BeautifulSoup
# import time as t
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from apscheduler.schedulers.twisted import TwistedScheduler


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

def run_crawl():
    runner = CrawlerRunner({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        })
    deferred = runner.crawl(StockSpider)
    # you can use reactor.callLater or task.deferLater to schedule a function
    deferred.addCallback(reactor.callLater, 5, run_crawl)
    return deferred

if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    scheduler = TwistedScheduler()
    scheduler.add_job(process.crawl, 'interval', args=[StockSpider], seconds=10)
    scheduler.start()
    process.start(False)


    

