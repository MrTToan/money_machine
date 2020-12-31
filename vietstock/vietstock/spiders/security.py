import scrapy
from datetime import datetime, date
from bs4 import BeautifulSoup
from ..items import VietstockItem

user_agent = 'Mozilla/5.0'
headers = {'User-Agent': user_agent }
class QuotesSpider(scrapy.Spider):
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


# https://stackoverflow.com/questions/3261858/does-anyone-have-example-code-for-a-sqlite-pipeline-in-scrapy
# https://stackoverflow.com/questions/62104734/scrapy-how-to-insert-data-into-sqlite
# https://stackoverflow.com/questions/8768439/how-to-give-delay-between-each-requests-in-scrapy#:~:text=if%20you%20want%20to%20keep,the%20website%20you%20are%20crawling.

    

