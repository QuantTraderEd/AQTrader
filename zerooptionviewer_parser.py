# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 20:38:29 2015

@author: assa
"""


def convert(strprice):
    return '%.2f' %round(float(strprice),2)

names = [
    'ShortCD',
    'FeedSource',
    'TAQ',
    'SecuritiesType',
    'Time',
    'BuySell',
    'LastPrice', 'LastQty',
    'Bid1', 'Ask1','BidQty1', 'AskQty1','BidCnt1', 'AskCnt1',
    'Bid2', 'Ask2','BidQty2', 'AskQty2','BidCnt2', 'AskCnt2',
    'Bid3', 'Ask3','BidQty3', 'AskQty3','BidCnt3', 'AskCnt3',
    'Bid4', 'Ask4','BidQty4', 'AskQty4','BidCnt4', 'AskCnt4',
    'Bid5', 'Ask5','BidQty5', 'AskQty5','BidCnt5', 'AskCnt5',
    'TotalBidQty', 'TotalAskQty',
    'TotalBidCnt', 'TotalAskCnt']

#msg = ''
#nightshift = 0

def msgParser(msg, nightshift, returntype=dict, count=-1):
    lst = msg.split(',')
    timestamp = lst[0]
    feedsource = lst[1]
    TAQ = lst[2]
    SecuritiesType = lst[3]
    buysell = ''
    lastprice = ''
    lastqty = ''

    if lst[1] == 'cybos' and lst[2] == 'Q' and lst[3] == 'futures':
        shcode = str(lst[4]) + '000'
        if nightshift == 0:
            ask1 = convert(lst[6])
            ask2 = convert(lst[7])
            ask3 = convert(lst[8])
            ask4 = convert(lst[9])
            ask5 = convert(lst[10])
            bid1 = convert(lst[23])
            bid2 = convert(lst[24])
            bid3 = convert(lst[25])
            bid4 = convert(lst[26])
            bid5 = convert(lst[27])
            askqty1 = str(lst[11])
            askqty2 = str(lst[12])
            askqty3 = str(lst[13])
            askqty4 = str(lst[14])
            askqty5 = str(lst[15])
            totalaskqty = str(lst[16])
            askcnt1 = str(lst[17])
            askcnt2 = str(lst[18])
            askcnt3 = str(lst[19])
            askcnt4 = str(lst[20])
            askcnt5 = str(lst[21])
            totalaskcnt = str(lst[22])
            bidqty1 = str(lst[28])
            bidqty2 = str(lst[29])
            bidqty3 = str(lst[30])
            bidqty4 = str(lst[31])
            bidqty5 = str(lst[32])
            totalbidqty = str(lst[33])
            bidcnt1 = str(lst[34])
            bidcnt2 = str(lst[35])
            bidcnt3 = str(lst[36])
            bidcnt4 = str(lst[37])
            bidcnt5 = str(lst[38])
            totalbidcnt = str(lst[39])

        else:
            ask1 = convert(lst[29])
            bid1 = convert(lst[18])
            askqty1 = str(lst[30])
            bidqty1 = str(lst[19])

            ask2 = convert(lst[27])
            bid2 = convert(lst[20])
            askqty2 = str(lst[28])
            bidqty2 = str(lst[21])

            ask3 = convert(lst[29])
            bid3 = convert(lst[22])
            askqty3 = str(lst[30])
            bidqty3 = str(lst[23])

            ask4 = convert(lst[31])
            bid4 = convert(lst[24])
            askqty4 = str(lst[32])
            bidqty4 = str(lst[25])

            ask5 = convert(lst[33])
            bid5 = convert(lst[26])
            askqty5 = str(lst[34])
            bidqty5 = str(lst[27])


            totalaskqty = str(lst[28])
            totalbidqty = str(lst[17])[:-2]

            bidcnt1 = str(lst[40])
            bidcnt2 = str(lst[41])
            bidcnt3 = str(lst[42])
            bidcnt4 = str(lst[43])
            bidcnt5 = str(lst[44])
            totalbidcnt = str(lst[39])

            askcnt1 = str(lst[46])
            askcnt2 = str(lst[47])
            askcnt3 = str(lst[48])
            askcnt4 = str(lst[49])
            askcnt5 = str(lst[50])
            totalaskcnt = str(lst[45])

        taqlist = [shcode,str(lst[1]),str(lst[2]),str(lst[3]),timestamp,
                   buysell, lastprice, lastqty,
                   bid1,ask1,bidqty1,askqty1,bidcnt1,askcnt1,
                   bid2,ask2,bidqty2,askqty2,bidcnt2,askcnt2,
                   bid3,ask3,bidqty3,askqty3,bidcnt3,askcnt3,
                   bid4,ask4,bidqty4,askqty4,bidcnt4,askcnt4,
                   bid5,ask5,bidqty5,askqty5,bidcnt5,askcnt5,
                   totalbidqty,totalaskqty,totalbidcnt,totalaskcnt]

    elif lst[1] == 'cybos' and lst[2] == 'Q' and lst[3] == 'options':
        shcode = str(lst[4])
        ask1 = convert(lst[6])
        ask2 = convert(lst[7])
        ask3 = convert(lst[8])
        ask4 = convert(lst[9])
        ask5 = convert(lst[10])
        bid1 = convert(lst[23])
        bid2 = convert(lst[24])
        bid3 = convert(lst[25])
        bid4 = convert(lst[26])
        bid5 = convert(lst[27])
        askqty1 = str(lst[11])
        askqty2 = str(lst[12])
        askqty3 = str(lst[13])
        askqty4 = str(lst[14])
        askqty5 = str(lst[15])
        totalaskqty = str(lst[16])
        askcnt1 = str(lst[17])
        askcnt2 = str(lst[18])
        askcnt3 = str(lst[19])
        askcnt4 = str(lst[20])
        askcnt5 = str(lst[21])
        totalaskcnt = str(lst[22])
        bidqty1 = str(lst[28])
        bidqty2 = str(lst[29])
        bidqty3 = str(lst[30])
        bidqty4 = str(lst[31])
        bidqty5 = str(lst[32])
        totalbidqty = str(lst[33])
        bidcnt1 = str(lst[34])
        bidcnt2 = str(lst[35])
        bidcnt3 = str(lst[36])
        bidcnt4 = str(lst[37])
        bidcnt5 = str(lst[38])
        totalbidcnt = str(lst[39])

        taqlist = [shcode, str(lst[1]), str(lst[2]), str(lst[3]), timestamp,
                   buysell, lastprice, lastqty,
                   bid1, ask1, bidqty1, askqty1, bidcnt1, askcnt1,
                   bid2, ask2, bidqty2, askqty2, bidcnt2, askcnt2,
                   bid3, ask3, bidqty3, askqty3, bidcnt3, askcnt3,
                   bid4, ask4, bidqty4, askqty4, bidcnt4, askcnt4,
                   bid5, ask5, bidqty5, askqty5, bidcnt5, askcnt5,
                   totalbidqty, totalaskqty, totalbidcnt, totalaskcnt]

    elif lst[1] == 'cybos' and lst[2] == 'E' and lst[3] == 'options':
        shcode = str(lst[4])
        expectprice = convert(lst[6])
        expectqty = ''
        taqlist = [shcode, str(lst[1]), str(lst[2]), str(lst[3]), timestamp,
                   buysell, expectprice, expectqty,
                   None, None, None, None, None, None,
                   None, None, None, None, None, None,
                   None, None, None, None, None, None,
                   None, None, None, None, None, None,
                   None, None, None, None, None, None,
                   None, None, None, None]

    elif lst[1] == 'xing' and lst[2] == 'T' and lst[3] == 'options':
        shcode = str(lst[31 + nightshift])
        lastprice = convert(lst[8 + nightshift])
        lastqty = str(lst[13 + nightshift])
        if lst[12 + nightshift] == '+':
            buysell = 'B'
        elif lst[12 + nightshift] == '-':
            buysell = 'S'
        else:
            buysell = ''
        bid1 = convert(lst[21 + nightshift])
        ask1 = convert(lst[20 + nightshift])
        taqlist = [shcode, str(lst[1]), str(lst[2]), str(lst[3]), timestamp,
                   buysell, lastprice, lastqty,
                   bid1, ask1, None, None, None, None,
                   None, None, None, None, None, None,
                   None, None, None, None, None, None,
                   None, None, None, None, None, None,
                   None, None, None, None, None, None,
                   None, None, None, None]

    elif lst[1] == 'xing' and lst[2] == 'T' and lst[3] == 'futures':
        shcode = str(lst[31 + nightshift])
        lastprice = convert(lst[8 + nightshift])
        lastqty = str(lst[13 + nightshift])
        if lst[12 + nightshift] == '+':
            buysell = 'B'
        elif lst[12 + nightshift] == '-':
            buysell = 'S'
        else:
            buysell = ''
        bid1 = convert(lst[22 + nightshift])
        ask1 = convert(lst[21 + nightshift])
        taqlist = [shcode, str(lst[1]), str(lst[2]), str(lst[3]), timestamp,
                   buysell, lastprice, lastqty,
                   bid1, ask1, None, None, None, None,
                   None, None, None, None, None, None,
                   None, None, None, None, None, None,
                   None, None, None, None, None, None,
                   None, None, None, None, None, None,
                   None, None, None, None]

    elif lst[1] == 'xing' and lst[2] == 'Q' and lst[3] == 'options':
        if nightshift == 1:
            shcode = str(lst[22])

            ask1 = convert(lst[6])
            ask2 = convert(lst[10])
            ask3 = convert(lst[14])

            bid1 = convert(lst[7])
            bid2 = convert(lst[11])
            bid3 = convert(lst[15])

            askqty1 = str(lst[8])
            askqty2 = str(lst[12])
            askqty3 = str(lst[16])

            bidqty1 = str(lst[9])
            bidqty2 = str(lst[13])
            bidqty3 = str(lst[17])


            totalaskqty = str(lst[18])
            totalbidqty = str(lst[19])

            totalaskcnt = str(lst[20])
            totalbidcnt = str(lst[21])

            taqlist = [shcode, str(lst[1]), str(lst[2]), str(lst[3]), timestamp,
                       buysell, lastprice, lastqty,
                       bid1, ask1, bidqty1, askqty1, None, None,
                       bid2, ask2, bidqty2, askqty2, None, None,
                       bid3, ask3, bidqty3, askqty3, None, None,
                       None, None, None, None, None, None,
                       None, None, None, None, None, None,
                       totalbidqty, totalaskqty, totalbidcnt, totalaskcnt]

    elif lst[1] == 'xing' and lst[2] == 'Q' and lst[3] == 'futures':
        if nightshift == 1:
            shcode = str(lst[40])

            ask1 = convert(lst[6])
            ask2 = convert(lst[12])
            ask3 = convert(lst[18])
            ask4 = convert(lst[24])
            ask5 = convert(lst[30])

            bid1 = convert(lst[7])
            bid2 = convert(lst[13])
            bid3 = convert(lst[19])
            bid4 = convert(lst[25])
            bid5 = convert(lst[31])

            askqty1 = str(lst[8])
            askqty2 = str(lst[14])
            askqty3 = str(lst[20])
            askqty4 = str(lst[26])
            askqty5 = str(lst[32])

            bidqty1 = str(lst[9])
            bidqty2 = str(lst[15])
            bidqty3 = str(lst[21])
            bidqty4 = str(lst[27])
            bidqty5 = str(lst[33])

            askcnt1 = str(lst[10])
            askcnt2 = str(lst[16])
            askcnt3 = str(lst[22])
            askcnt4 = str(lst[28])
            askcnt5 = str(lst[34])

            bidcnt1 = str(lst[11])
            bidcnt2 = str(lst[17])
            bidcnt3 = str(lst[23])
            bidcnt4 = str(lst[29])
            bidcnt5 = str(lst[35])

            totalaskqty = str(lst[36])
            totalbidqty = str(lst[37])

            totalaskcnt = str(lst[38])
            totalbidcnt = str(lst[39])

            taqlist = [shcode, str(lst[1]), str(lst[2]), str(lst[3]), timestamp,
                       buysell, lastprice, lastqty,
                       bid1, ask1, bidqty1, askqty1, bidcnt1, askcnt1,
                       bid2, ask2, bidqty2, askqty2, bidcnt2, askcnt2,
                       bid3, ask3, bidqty3, askqty3, bidcnt3, askcnt3,
                       bid4, ask4, bidqty4, askqty4, bidcnt4, askcnt4,
                       bid5, ask5, bidqty5, askqty5, bidcnt5, askcnt5,
                       totalbidqty, totalaskqty, totalbidcnt, totalaskcnt]

        pass

    if returntype == dict:
        taqdict = {}
        for i in xrange(len(names)):
            key = names[i]
            value = taqlist[i]
            taqdict[key] = value
        return taqdict
    elif returntype == list:
        return taqlist
    elif returntype == tuple:
        taqitem = []
        if taqlist[2] == 'Q':
            taqitem = taqlist[0:5] + taqlist[8:]
        elif taqlist[2] == 'T':
            taqitem = taqlist[0:5] + taqlist[6:8] + taqlist[5:6] +taqlist[8:10]
        elif taqlist[2] == 'E':
            taqitem = taqlist[0:5] + taqlist[6:7] + taqlist[5:6]
        if count >= 0: taqitem.insert(0, count)
        return tuple(taqitem)

if __name__ == '__main__':
    import zmq
    import datetime as dt

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://127.0.0.1:5500")
    socket.setsockopt(zmq.SUBSCRIBE, "")

    while True:
        nowtime = dt.datetime.now()
        strnowtime = dt.datetime.strftime(nowtime,'%H:%M:%S.%f')[:-3]

        nightshift = 0
        if 7 <= nowtime.hour < 17:
            nightshift = 0
        else:
            nightshift = 1

        msg = socket.recv()
        row = msgParser(msg,nightshift=nightshift)
        print row['Time'], row['ShortCD'], row['LastPrice']
