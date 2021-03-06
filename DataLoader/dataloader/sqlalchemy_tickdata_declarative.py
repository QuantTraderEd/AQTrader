# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

# from sqlalchemy import create_engine

Base = declarative_base()


class TickData(Base):
    __tablename__ = 'TickData'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    # id = Column(Integer, primary_key=True, nullable=False)
    shortcd = Column(String)
    feedsource = Column(String)
    taq = Column(String)
    securitiestype = Column(String)
    datetime = Column(DateTime)
    buysell = Column(String)
    lastprice = Column(Float)
    lastqty = Column(Integer)
    bid1 = Column(Float)
    bid2 = Column(Float)
    bid3 = Column(Float)
    bid4 = Column(Float)
    bid5 = Column(Float)
    ask1 = Column(Float)
    ask2 = Column(Float)
    ask3 = Column(Float)
    ask4 = Column(Float)
    ask5 = Column(Float)
    bidqty1 = Column(Integer)
    bidqty2 = Column(Integer)
    bidqty3 = Column(Integer)
    bidqty4 = Column(Integer)
    bidqty5 = Column(Integer)
    askqty1 = Column(Integer)
    askqty2 = Column(Integer)
    askqty3 = Column(Integer)
    askqty4 = Column(Integer)
    askqty5 = Column(Integer)
    totalbidqty = Column(Integer)
    totalaskqty = Column(Integer)
    # only futures, options
    bidcnt1 = Column(Integer)
    bidcnt2 = Column(Integer)
    bidcnt3 = Column(Integer)
    bidcnt4 = Column(Integer)
    bidcnt5 = Column(Integer)
    askcnt1 = Column(Integer)
    askcnt2 = Column(Integer)
    askcnt3 = Column(Integer)
    askcnt4 = Column(Integer)
    askcnt5 = Column(Integer)
    totalbidcnt = Column(Integer)
    totalaskcnt = Column(Integer)
    # only equity, ETF
    bid6 = Column(Float)
    bid7 = Column(Float)
    bid8 = Column(Float)
    bid9 = Column(Float)
    bid10 = Column(Float)
    ask6 = Column(Float)
    ask7 = Column(Float)
    ask8 = Column(Float)
    ask9 = Column(Float)
    ask10 = Column(Float)
    bidqty6 = Column(Integer)
    bidqty7 = Column(Integer)
    bidqty8 = Column(Integer)
    bidqty9 = Column(Integer)
    bidqty10 = Column(Integer)
    askqty6 = Column(Integer)
    askqty7 = Column(Integer)
    askqty8 = Column(Integer)
    askqty9 = Column(Integer)
    askqty10 = Column(Integer)


# class FutOptTickData(TickData):
#     __tablename__ = 'FutOptTickData'
#     bidcnt1 = Column(Integer)
#     bidcnt2 = Column(Integer)
#     bidcnt3 = Column(Integer)
#     bidcnt4 = Column(Integer)
#     bidcnt5 = Column(Integer)
#     askcnt1 = Column(Integer)
#     askcnt2 = Column(Integer)
#     askcnt3 = Column(Integer)
#     askcnt4 = Column(Integer)
#     askcnt5 = Column(Integer)
#     totalbidcnt = Column(Integer)
#     totalaskcnt = Column(Integer)
#
#
# class EquityTickData(TickData):
#     __tablename__ = 'EquityTickData'
#     bid6 = Column(Float)
#     bid7 = Column(Float)
#     bid8 = Column(Float)
#     bid9 = Column(Float)
#     bid10 = Column(Float)
#     ask6 = Column(Float)
#     ask7 = Column(Float)
#     ask8 = Column(Float)
#     ask9 = Column(Float)
#     ask10 = Column(Float)
#     bidqty6 = Column(Integer)
#     bidqty7 = Column(Integer)
#     bidqty8 = Column(Integer)
#     bidqty9 = Column(Integer)
#     bidqty10 = Column(Integer)
#     askqty6 = Column(Integer)
#     askqty7 = Column(Integer)
#     askqty8 = Column(Integer)
#     askqty9 = Column(Integer)
#     askqty10 = Column(Integer)
