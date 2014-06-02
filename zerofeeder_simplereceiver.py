# -*- coding: utf-8 -*-
"""
Created on Mon Jun 02 20:17:20 2014

@author: assa
"""

import zmq

def convert(strprice):
    return (str(round(float(strprice),2)))

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:5500")
socket.setsockopt(zmq.SUBSCRIBE,"")

while True:
    msg =  socket.recv()
    lst = msg.split(',')
    print msg
    if lst[0] == 'xing' and lst[1] == 'T' and lst[2] == 'futures':        
        timestamp = lst[0]
        feedtype = lst[1]
        securitiestype = lst[2]
        shcode = lst[31]
        bidqty = ''
        bid = lst[21]
        offer = lst[20]
        offerqty = ''
        price = lst[7]
        cvolume = lst[12]   
        cgubun = lst[11]
        msglst = [timestamp,feedtype,securitiestype,shcode,bidqty,bid,offer,offerqty,price,cvolume,cgubun]                        
        msg = ','.join(msglst)
        print msg
        pass
    elif lst[0] == 'cybos' and lst[1] == 'Q' and lst[2] == 'futures':
        timestamp = lst[0]
        feedtype = lst[1]
        securitiestype = lst[2]
        
        shcode = lst[3]        
        
        ask1 = lst[5]
        bid1 = lst[22]
        askqty1 = lst[10]
        bidqty1 = lst[27]
        askcnt1 = lst[16]
        bidcnt1 = lst[33]
        
        ask2 = lst[6]
        bid2 = lst[23]
        askqty2 = lst[11]
        bidqty2 = lst[28]
        askcnt2 = lst[17]
        bidcnt2 = lst[34]
        
        ask3 = lst[7]
        bid3 = lst[24]
        askqty3 = lst[12]
        bidqty3 = lst[29]
        askcnt3 = lst[18]
        bidcnt3 = lst[35]
        
        ask4 = lst[8]
        bid4 = lst[25]
        askqty4 = lst[13]        
        bidqty4 = lst[30]
        askcnt4 = lst[19]
        bidcnt4 = lst[36]
                
        ask5 = lst[9]
        bid5 = lst[26]
        askqty5 = lst[14]
        bidqty5 = lst[31]
        askcnt5 = lst[20]
        bidcnt5 = lst[37]
                        
        totalaskqty = lst[15]
        totalbidqty = lst[32]
        
        totalaskcnt = lst[21]
        totalbidcnt = lst[38]        
        
        msglst = [timestamp,feedtype,securitiestype,shcode,
                  bid1,bid2,bid3,bid4,bid5,
                  ask1,ask2,ask3,ask4,ask5,
                  bidqty1,bidqty2,bidqty3,bidqty4,bidqty5,
                  askqty1,askqty2,askqty3,askqty4,askqty5,
                  bidcnt1,bidcnt2,bidcnt3,bidcnt4,bidcnt5,
                  askcnt1,askcnt2,askcnt3,askcnt4,askcnt5,
                  totalbidqty,totalaskqty,totalbidcnt,totalaskcnt
                  ]                          
        
        msg = ','.join(msglst)
        print msg
        pass
    elif lst[0] == 'xing' and lst[1] == 'T' and lst[2] == 'options':
        timestamp = lst[0]
        feedtype = lst[1]
        securitiestype = lst[2]
        
        shcode = lst[30]
        bidqty = ''
        bid = lst[21]
        offer = lst[20]
        offerqty = ''
        price = lst[7]
        cvolume = lst[12]   
        cgubun = lst[11]
        msglst = [timestamp,feedtype,securitiestype,shcode,bidqty,bid,offer,offerqty,price,cvolume,cgubun]                        
        msg = ','.join(msglst)
        print msg
        pass
    elif lst[0] == 'cybos' and lst[1] == 'Q' and lst[2] == 'options':
        timestamp = lst[0]
        feedtype = lst[1]
        securitiestype = lst[2]
        
        shcode = lst[3]        
        
        ask1 = lst[5]
        bid1 = lst[22]
        askqty1 = lst[10]
        bidqty1 = lst[27]
        askcnt1 = lst[16]
        bidcnt1 = lst[33]
        
        ask2 = lst[6]
        bid2 = lst[23]
        askqty2 = lst[11]
        bidqty2 = lst[28]
        askcnt2 = lst[17]
        bidcnt2 = lst[34]
        
        ask3 = lst[7]
        bid3 = lst[24]
        askqty3 = lst[12]
        bidqty3 = lst[29]
        askcnt3 = lst[18]
        bidcnt3 = lst[35]
        
        ask4 = lst[8]
        bid4 = lst[25]
        askqty4 = lst[13]        
        bidqty4 = lst[30]
        askcnt4 = lst[19]
        bidcnt4 = lst[36]
                
        ask5 = lst[9]
        bid5 = lst[26]
        askqty5 = lst[14]
        bidqty5 = lst[31]
        askcnt5 = lst[20]
        bidcnt5 = lst[37]
                        
        totalaskqty = lst[15]
        totalbidqty = lst[32]
        
        totalaskcnt = lst[21]
        totalbidcnt = lst[38]        
        
        
        
        msglst = [timestamp,feedtype,securitiestype,shcode,
                  bid1,bid2,bid3,bid4,bid5,
                  ask1,ask2,ask3,ask4,ask5,
                  bidqty1,bidqty2,bidqty3,bidqty4,bidqty5,
                  askqty1,askqty2,askqty3,askqty4,askqty5,
                  bidcnt1,bidcnt2,bidcnt3,bidcnt4,bidcnt5,
                  askcnt1,askcnt2,askcnt3,askcnt4,askcnt5,
                  totalbidqty,totalaskqty,totalbidcnt,totalaskcnt
                  ]                
        
        
        msg = ','.join(msglst)
        print msg
        pass
        
        
    