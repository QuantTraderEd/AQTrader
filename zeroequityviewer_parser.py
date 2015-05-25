# -*- coding: utf-8 -*-
"""
Created on Fri May 15 20:38:29 2015

@author: assa
"""

names = [
    'ShortCD',
    'FeedSource',
    'TAQ',
    'SecuritiesType',
    'Time',
    'BuySell',
    'LastPrice', 'LastQty',
    'Bid1', 'Ask1', 'BidQty1', 'AskQty1',
    'Bid2', 'Ask2', 'BidQty2', 'AskQty2',
    'Bid3', 'Ask3', 'BidQty3', 'AskQty3',
    'Bid4', 'Ask4', 'BidQty4', 'AskQty4',
    'Bid5', 'Ask5', 'BidQty5', 'AskQty5',
    'Bid6', 'Ask6', 'BidQty6', 'AskQty6',
    'Bid7', 'Ask7', 'BidQty7', 'AskQty7',
    'Bid8', 'Ask8', 'BidQty8', 'AskQty8',
    'Bid9', 'Ask9', 'BidQty9', 'AskQty9',
    'Bid10', 'Ask10', 'BidQty10', 'AskQty10',
    'TotalBidQty', 'TotalAskQty'
    ]


def msgParser(msg, returntype=dict, count=-1):
    lst = msg.split(',')
    timestamp = lst[0]
    feedsource = str(lst[1])
    TAQ = str(lst[2])
    SecuritiesType = str(lst[3])
    buysell = ''
    lastprice = ''
    lastqty = ''

    if lst[1] == 'cybos' and lst[2] == 'Q' and lst[3] == 'equity':
        shortcd = str(lst[4])

        ask1 = str(lst[7])
        bid1 = str(lst[8])
        askqty1 = str(lst[9])
        bidqty1 = str(lst[10])

        ask2 = str(lst[11])
        bid2 = str(lst[12])
        askqty2 = str(lst[13])
        bidqty2 = str(lst[14])

        ask3 = str(lst[15])
        bid3 = str(lst[16])
        askqty3 = str(lst[17])
        bidqty3 = str(lst[18])

        ask4 = str(lst[19])
        bid4 = str(lst[20])
        askqty4 = str(lst[21])
        bidqty4 = str(lst[22])

        ask5 = str(lst[23])
        bid5 = str(lst[24])
        askqty5 = str(lst[25])
        bidqty5 = str(lst[26])

        totalaskqty = str(lst[27])
        totalbidqty = str(lst[28])
        # totalbidqty = str(lst[17])[:-2]

        ask6 = str(lst[31])
        bid6 = str(lst[32])
        askqty6 = str(lst[33])
        bidqty6 = str(lst[34])

        ask7 = str(lst[35])
        bid7 = str(lst[36])
        askqty7 = str(lst[37])
        bidqty7 = str(lst[38])

        ask8 = str(lst[39])
        bid8 = str(lst[40])
        askqty8 = str(lst[41])
        bidqty8 = str(lst[42])

        ask9 = str(lst[43])
        bid9 = str(lst[44])
        askqty9 = str(lst[45])
        bidqty9 = str(lst[46])

        ask10 = str(lst[47])
        bid10 = str(lst[48])
        askqty10 = str(lst[49])
        bidqty10 = str(lst[50])

        taqlist = [shortcd, feedsource, TAQ, SecuritiesType, timestamp,
                   buysell, lastprice, lastqty,
                   bid1, ask1, bidqty1, askqty1,
                   bid2, ask2, bidqty2, askqty2,
                   bid3, ask3, bidqty3, askqty3,
                   bid4, ask4, bidqty4, askqty4,
                   bid5, ask5, bidqty5, askqty5,
                   bid6, ask6, bidqty6, askqty6,
                   bid7, ask7, bidqty7, askqty7,
                   bid8, ask8, bidqty8, askqty8,
                   bid9, ask9, bidqty9, askqty9,
                   bid10, ask10, bidqty10, askqty10,
                   totalbidqty, totalaskqty]

    elif lst[1] == 'xing' and lst[2] == 'T' and lst[3] == 'equity':
        shortcd = 'A' + str(lst[26])
        lastprice = str(lst[8])
        lastqty = str(lst[13])
        # Volume = str(lst[14])
        if lst[12] == '+':
            buysell = 'B'
        elif lst[12] == '-':
            buysell = 'S'
        else:
            buysell = ''
        bid1 = str(lst[23])
        ask1 = str(lst[22])

        taqlist = [shortcd, feedsource, TAQ, SecuritiesType, timestamp,
                   buysell, lastprice, lastqty,
                   bid1, ask1, None, None,
                   None, None, None, None,
                   None, None, None, None,
                   None, None, None, None,
                   None, None, None, None,
                   None, None, None, None,
                   None, None, None, None,
                   None, None, None, None,
                   None, None, None, None,
                   None, None, None, None,
                   None, None]

    elif lst[1] == 'xing' and lst[2] == 'E' and lst[3] == 'equity':
        shortcd = 'A' + str(lst[14])
        expectprice = str(lst[5])
        expectqty = str(lst[6])
        # expectrate = str(lst[9])
        ask1 = str(lst[10])
        bid1 = str(lst[11])
        askqty1 = str(lst[12])
        bidqty1 = str(lst[13])
        taqlist = [shortcd, feedsource, TAQ, SecuritiesType, timestamp,
                   buysell, expectprice, expectqty,
                   bid1, ask1, bidqty1, askqty1,
                   None, None, None, None,
                   None, None, None, None,
                   None, None, None, None,
                   None, None, None, None,
                   None, None, None, None,
                   None, None, None, None,
                   None, None, None, None,
                   None, None, None, None,
                   None, None, None, None,
                   None, None]
    elif lst[1] == 'xing' and lst[2] == 'N' and lst[3] == 'equity':
        return None
    else:
        return None

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
            taqitem = taqlist[0:5] + taqlist[6:8] + taqlist[5:6] + taqlist[8:10]
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
        strnowtime = dt.datetime.strftime(nowtime, '%H:%M:%S.%f')[:-3]

        msg = socket.recv()
        row = msgParser(msg)
        if not row:
            print row['Time'], row['ShortCD'], row['LastPrice']


