#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017-09-22 michael_yin
#

from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, SmallInteger, String, Date, DateTime, Float, Boolean, Text, LargeBinary)

from scrapy.utils.project import get_project_settings

DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"), pool_size=32, max_overflow=0)


def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class Products(DeclarativeBase):
    __tablename__ = "products"
    code = Column(String(20), primary_key=True)
    url = Column(String(150))
    title = Column(String(100))
    price = Column(Float)
    unit = Column(String(5))
    prices = Column(String(1000))
    min_price = Column(Float)
    avg_price = Column(Float)
    last_date = Column(Date)
    store = Column(String(10))



