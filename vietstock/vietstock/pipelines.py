# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging

from scrapy import signals
from sqlalchemy import Column, Integer, String, DateTime, Date, Float
from sqlalchemy import create_engine 
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

logger = logging.getLogger(__name__)

DeclaretiveBase = declarative_base()


class Following(DeclaretiveBase):
    __tablename__ = "following"

    id = Column(Integer, primary_key=True)
    date = Column('date', String)
    time = Column('time', DateTime)
    stock_name = Column('stock_name', String)
    price = Column('price', Float)

    def __repr__(self):
        return "<Logging({})>".format(self.stock_name)

class SqlitePipeline(object):
    def __init__(self, settings):
        self.database = settings.get('DATABASE')
        self.sessions = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls(crawler.settings)
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline 

    def create_engine(self):
        engine = create_engine(URL(**self.database), poolclass=NullPool) #, connect_args = {'charset':'utf8'}
        return engine

    def create_tables(self, engine):
        DeclaretiveBase.metadata.create_all(engine, checkfirst=True)

    def create_session(self, engine):
        session = sessionmaker(bind=engine)()
        return session 

    def spider_opened(self, spider):
        engine = self.create_engine()
        self.create_tables(engine)
        session = self.create_session(engine)
        self.sessions[spider] = session 

    def spider_closed(self, spider):
        session = self.sessions.pop(spider)
        session.close()

    def process_item(self, item, spider):
        session = self.sessions[spider]
        following = Following(**item)
        link_exists = session.query(Following).filter_by(stock_name=item['stock_name']).first() is not None 

        if link_exists:
            logger.info('Item {} is in db'.format(following))
            return item

        try:
            session.add(following)
            session.commit()
            logger.info('Item {} stored in db'.format(following))
        except:
            logger.info('Failed to add {} to db'.format(following))
            session.rollback()
            raise 

        return item
