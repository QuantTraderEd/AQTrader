# -*- coding: utf-8 -*-
"""
Created on Mon Jun 02 20:17:20 2014

@author: assa
"""

import zmq
import datetime

def convert(strprice):
    return (str(round(float(strprice),2)))

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:5500")
socket.setsockopt(zmq.SUBSCRIBE,"")

filep = open("test.txt",'w+')
cvolume = 0

while True:
    msg =  socket.recv()
    lst = msg.split(',')
    nowtime = datetime.datetime.now()
    if lst[1] == 'xing' and lst[2] == 'T' and lst[3] == 'futures':        
        timestamp = lst[0]
        APItype = lst[1]
        FeedType = lst[2]
        ProductType = lst[3]
        
        shcode = lst[32]
        bidqty = ''
        bid = lst[22]
        offer = lst[21]
        offerqty = ''
        price = lst[8]
        cvolume = lst[13]   
        cgubun = lst[12]
        msglst = [timestamp,FeedType,ProductType,shcode,bidqty,bid,offer,offerqty,price,cvolume,cgubun]                        
        msg = ','.join(msglst)
        print msg
        filep.write(msg+'\n')
        pass
    elif lst[1] == 'cybos' and lst[2] == 'Q' and lst[3] == 'futures':
        timestamp = lst[0]
        APItype = lst[1]
        FeedType = lst[2]
        ProductType = lst[3]
        
        shcode = lst[4]     
        
        if nowtime.hour >= 7 and nowtime.hour < 18:
            ask1 = convert(lst[6])
            bid1 = convert(lst[23])
            askqty1 = lst[11]
            bidqty1 = lst[28]
            askcnt1 = lst[17]
            bidcnt1 = lst[34]
            
            ask2 = convert(lst[7])
            bid2 = convert(lst[24])
            askqty2 = lst[12]
            bidqty2 = lst[29]
            askcnt2 = lst[18]
            bidcnt2 = lst[35]
            
            ask3 = convert(lst[8])
            bid3 = convert(lst[25])
            askqty3 = lst[13]
            bidqty3 = lst[30]
            askcnt3 = lst[19]
            bidcnt3 = lst[36]
            
            ask4 = convert(lst[9])
            bid4 = convert(lst[26])
            askqty4 = lst[14]        
            bidqty4 = lst[31]
            askcnt4 = lst[20]
            bidcnt4 = lst[37]
                    
            ask5 = convert(lst[10])
            bid5 = convert(lst[27])
            askqty5 = lst[15]
            bidqty5 = lst[32]
            askcnt5 = lst[21]
            bidcnt5 = lst[38]
                            
            totalaskqty = lst[16]
            totalbidqty = lst[33]
            
            totalaskcnt = lst[22]
            totalbidcnt = lst[39]        
            
            msglst = [timestamp,FeedType,ProductType,shcode,
                      bid1,bid2,bid3,bid4,bid5,
                      ask1,ask2,ask3,ask4,ask5,
                      bidqty1,bidqty2,bidqty3,bidqty4,bidqty5,
                      askqty1,askqty2,askqty3,askqty4,askqty5,
                      bidcnt1,bidcnt2,bidcnt3,bidcnt4,bidcnt5,
                      askcnt1,askcnt2,askcnt3,askcnt4,askcnt5,
                      totalbidqty,totalaskqty,totalbidcnt,totalaskcnt
                      ]                          
            
            msg = ','.join(msglst)
            #print msg
            filep.write(msg+'\n')
        else:
            ask1 = convert(lst[29])
            bid1 = convert(lst[18])
            askqty1 = lst[30]
            bidqty1 = lst[19]
            askcnt1 = lst[46]
            bidcnt1 = lst[40]
            
            ask2 = convert(lst[31])
            bid2 = convert(lst[20])
            askqty2 = lst[32]
            bidqty2 = lst[21]
            askcnt2 = lst[47]
            bidcnt2 = lst[41]
            
            ask3 = convert(lst[33])
            bid3 = convert(lst[22])
            askqty3 = lst[34]
            bidqty3 = lst[23]
            askcnt3 = lst[48]
            bidcnt3 = lst[42]
            
            ask4 = convert(lst[35])
            bid4 = convert(lst[24])
            askqty4 = lst[36]        
            bidqty4 = lst[25]
            askcnt4 = lst[49]
            bidcnt4 = lst[43]
                    
            ask5 = convert(lst[37])
            bid5 = convert(lst[26])
            askqty5 = lst[38]
            bidqty5 = lst[27]
            askcnt5 = lst[50]
            bidcnt5 = lst[44]
                            
            totalaskqty = lst[28]
            totalbidqty = lst[17]
            
            totalaskcnt = lst[45]
            totalbidcnt = lst[39]        
            
            
            if cvolume != lst[13]:
                lastprice = convert(lst[5])
                lastqty = str(int(lst[13]) - int(cvolume))
                cvolume = lst[13]
            else:
                lastprice = ''
                lastqty = ''
                
#            msglst = [timestamp,APItype,FeedType,ProductType,shcode,
#                      bid1,bid2,bid3,bid4,bid5,
#                      ask1,ask2,ask3,ask4,ask5,
#                      bidqty1,bidqty2,bidqty3,bidqty4,bidqty5,
#                      askqty1,askqty2,askqty3,askqty4,askqty5,
#                      bidcnt1,bidcnt2,bidcnt3,bidcnt4,bidcnt5,
#                      askcnt1,askcnt2,askcnt3,askcnt4,askcnt5,
#                      totalbidqty,totalaskqty,totalbidcnt,totalaskcnt
#                      ]                          
            msglst = [timestamp,APItype,FeedType,ProductType,shcode,
                   askqty1,ask1,bid1,bidqty1,lastprice,lastqty]
            msg = ','.join(msglst)
            print msg
        pass
    elif lst[1] == 'xing' and lst[2] == 'T' and lst[3] == 'options':
        timestamp = lst[0]
        APItype = lst[1]
        FeedType = lst[2]
        ProductType = lst[3]
        
        shcode = lst[31]
        bidqty = ''
        bid = lst[22]
        offer = lst[21]
        offerqty = ''
        price = lst[8]
        cvolume = lst[13]   
        cgubun = lst[12]
        msglst = [timestamp,FeedType,ProductType,shcode,bidqty,bid,offer,offerqty,price,cvolume,cgubun]                        
        msg = ','.join(msglst)
        print msg
        filep.write(msg+'\n')
        pass
    elif lst[1] == 'cybos' and lst[2] == 'Q' and lst[3] == 'options':
        timestamp = lst[0]
        APItype = lst[1]
        FeedType = lst[2]
        ProductType = lst[3]
        
        shcode = lst[4]        
        
        ask1 = convert(lst[6])
        bid1 = convert(lst[23])
        askqty1 = lst[11]
        bidqty1 = lst[28]
        askcnt1 = lst[17]
        bidcnt1 = lst[34]
        
        ask2 = convert(lst[7])
        bid2 = convert(lst[24])
        askqty2 = lst[12]
        bidqty2 = lst[29]
        askcnt2 = lst[18]
        bidcnt2 = lst[35]
        
        ask3 = convert(lst[8])
        bid3 = convert(lst[25])
        askqty3 = lst[14]
        bidqty3 = lst[30]
        askcnt3 = lst[19]
        bidcnt3 = lst[36]
        
        ask4 = convert(lst[9])
        bid4 = convert(lst[26])
        askqty4 = lst[14]        
        bidqty4 = lst[31]
        askcnt4 = lst[20]
        bidcnt4 = lst[37]
                
        ask5 = convert(lst[10])
        bid5 = convert(lst[27])
        askqty5 = lst[15]
        bidqty5 = lst[32]
        askcnt5 = lst[21]
        bidcnt5 = lst[38]
                        
        totalaskqty = lst[16]
        totalbidqty = lst[33]
        
        totalaskcnt = lst[22]
        totalbidcnt = lst[39]        
        
        
        
        msglst = [timestamp,FeedType,ProductType,shcode,
                  bid1,bid2,bid3,bid4,bid5,
                  ask1,ask2,ask3,ask4,ask5,
                  bidqty1,bidqty2,bidqty3,bidqty4,bidqty5,
                  askqty1,askqty2,askqty3,askqty4,askqty5,
                  bidcnt1,bidcnt2,bidcnt3,bidcnt4,bidcnt5,
                  askcnt1,askcnt2,askcnt3,askcnt4,askcnt5,
                  totalbidqty,totalaskqty,totalbidcnt,totalaskcnt
                  ]                
        
        
        msg = ','.join(msglst)
        #print msg
        filep.write(msg+'\n')
        pass
    elif lst[1] == 'cybos' and lst[2] == 'E' and lst[3] == 'options':
        timestamp = lst[0]
        APItype = lst[1]
        FeedType = lst[2]
        ProductType = lst[3]
        
        shcode = lst[4]        
        expect = lst[6]
        
        msglst = [timestamp,FeedType,ProductType,shcode,expect]
        msg = ','.join(msglst)
        #print msg
        filep.write(msg+'\n')
        pass
        
        
        
    
    strdate = datetime.date.today().strftime('%Y%m%d')
    nowtime = datetime.datetime.now()
    endtime = datetime.datetime.strptime(strdate + '15:16:00','%Y%m%d%H:%M:%S')
    if nowtime > endtime: break

filep.close()
