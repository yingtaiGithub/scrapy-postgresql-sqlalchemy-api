# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
from datetime import date

from sqlalchemy.orm import sessionmaker
from scrapy_spider.models import db_connect, create_table, Products


class DBPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.

        """
        session = self.Session()

        code = re.search('stockcode=(\d+)', item['url']).group(1)
        row = session.query(Products).filter_by(code=code).first()
        if row:
            last_date = row.last_date
            if last_date != date.today() and item['price']:
                row.url = item['url']
                row.price = item['price']
                prices = [float(price) for price in row.prices.split()]
                prices.insert(0, float(item['price']))
                prices = prices[:180]
                row.prices = ' '.join([str(price) for price in prices])
                row.min_price = min(prices)
                row.avg_price = sum(prices)/len(prices)
                row.last_date = date.today()

                try:
                    session.commit()
                except:
                    session.rollback()
                    raise
                finally:
                    session.close()
        else:
            product = Products()
            product.code = re.search('stockcode=(\d+)', item['url']).group(1)
            product.url = item['url']
            product.title = item['title']
            product.price = item['price']
            product.unit = item['unit']
            product.prices = str(item['price'])
            product.min_price = item['price']
            product.avg_price = item['price']
            product.last_date = date.today()
            product.store = 'c'

            try:
                session.add(product)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()

        return item
