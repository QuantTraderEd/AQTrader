# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 13:38:05 2015

@author: assa
"""

from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import mapper

Base = declarative_base()
metadata = MetaData()



class Master(object):
    def __init__(self):
        self.shortcd = None
        self.name_en = None
        self.securitiestype = None
        self.expiredate = None


def get_mapping_masterclass(strdate):
    master = Table('master_' + strdate, metadata,            
            Column('shortcd', String(8), primary_key=True),
            Column('name_en', String(16)),
            Column('securitiestype', String(16)),
            Column('expiredate', Date)
        )
    mapper(Master, master)
    return Master
    pass        

eng = create_engine('sqlite:///master.db')



if __name__ == '__main__':
    import datetime as dt
    from sqlalchemy.orm import sessionmaker
    
    # Base.metadata.bind = eng
    # Base.metadata.create_all()
    Master = get_mapping_masterclass('20151023')
    metadata.bind = eng
    metadata.create_all()
    
    Session = sessionmaker(bind=eng)
    session = Session()
    
    
    master_instance = Master()
    master_instance.shortcd = '201KB250'
    master_instance.securitiestype = 'Options'
    master_instance.name_en = 'C 1511 250'
    master_instance.expiredate = dt.date(2015, 11, 12)
    
    session.add(master_instance)
    session.commit()
    
    rs = session.query(Master).all()

    for instance in rs:
        print instance.shortcd, instance.securitiestype, instance.expiredate
