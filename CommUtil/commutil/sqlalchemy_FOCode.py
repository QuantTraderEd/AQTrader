# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 17:53:48 2015

@author: assa
"""

import sqlalchemy_declarative as declarative
import datetime as dt
from sqlalchemy.orm import sessionmaker

nowdate = dt.date.today()
#nowdate = dt.date(2015, 10, 23)

Master = declarative.get_mapping_masterclass(nowdate.strftime('%Y%m%d'))
declarative.metadata.bind = declarative.eng
declarative.metadata.create_all()

Session = sessionmaker(bind=declarative.eng)
session = Session()

def insertFOInfo(shortcd, name_en, securitiestype, expiredate):
    master_instance = Master()
    master_instance.shortcd = shortcd
    master_instance.name_en = name_en
    master_instance.securitiestype = securitiestype
    master_instance.expiredate = expiredate
    
    session.add(master_instance)
    

if __name__ == '__main__':
    import time
    import pycybos as pc
    FutureCode = pc.CpFutureCode()
    OptionCode = pc.CpOptionCode()
    
    t1 = time.time()
    
    if nowdate.isoweekday() < 6:
        for i in xrange(FutureCode.GetCount()):
            shortcd = FutureCode.GetData('0', i)
            name_en = FutureCode.GetData('1', i)
            securitiestype = 'Futures'
            #expiredate = dt.date(2015, 11, 18)
            print shortcd, name_en, securitiestype
            insertFOInfo(shortcd, name_en, securitiestype, None)
            
        for i in xrange(OptionCode.GetCount()):
            shortcd = OptionCode.GetData('0', i)
            name_en = OptionCode.GetData('1', i)
            securitiestype = 'Options'
            # expiredate = dt.date(2015, 11, 18)
            expiredate = OptionCode.GetData('3', i)
            print shortcd, 'KOSPI200 ' + name_en, securitiestype
            insertFOInfo(shortcd, 'KOSPI200 ' + name_en, securitiestype, None)
            
        session.commit()
        
        print 'elcpse time: ', time.time() - t1
        
        rs = session.query(Master).all()
        
        print len(rs)    
    else:
        print 'no bizdate...'
    
    
#    for instance in rs:
#        print instance.shortcd, instance.name_en, instance.securitiestype, instance.expiredate
    