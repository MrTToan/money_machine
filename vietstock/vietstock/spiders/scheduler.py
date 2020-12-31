from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from .security import StockSpider

def crawl_job():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(StockSpider)
    # runner = CrawlerRunner(settings)
    return process.start()

def schedule_next_crawl(null, sleep_time):
    print('Wait')
    reactor.callLater(sleep_time, crawl)

def crawl():
    d = crawl_job()
    print('Done Crawl')
    # d.addBoth(lambda _: reactor.stop())
    d.addCallback(schedule_next_crawl, 30)
    d.addErrback(catch_error)

def catch_error(failure):
    print(failure.value)

if __name__ == '__main__':
    crawl()
    print('Done')
    reactor.run()