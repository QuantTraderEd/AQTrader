from sqlalchemy_tickdata_declarative import TickData


def insertNewTickData(session, msg_dict):
    shortcd = msg_dict['ShortCD']
    feedsource = msg_dict['FeedSource']
    taq = msg_dict['TAQ']
    securitiestype = msg_dict['SecuritiesType']
    timestamp = msg_dict['TimeStamp']

    if taq == 'T':
        buysell = msg_dict['BuySell']
        lastprice = msg_dict['LastPrice']
        lastqty = msg_dict['LastQty']

        bid1 = msg_dict['Bid1']
        ask1 = msg_dict['Ask1']

        new_tickdata = TickData(shortcd=shortcd,
                                feedsource=feedsource,
                                taq=taq,
                                securitiestype=securitiestype,
                                datetime=timestamp,
                                buysell=buysell,
                                lastprice=lastprice,
                                lastqty=lastqty,
                                bid1=bid1,
                                ask1=ask1,
                                )

    elif taq == 'Q':
        bid1 = msg_dict['Bid1']
        bid2 = msg_dict['Bid2']
        bid3 = msg_dict['Bid3']

        ask1 = msg_dict['Ask1']
        ask2 = msg_dict['Ask2']
        ask3 = msg_dict['Ask3']

        bidqty1 = msg_dict['BidQty1']
        bidqty2 = msg_dict['BidQty2']
        bidqty3 = msg_dict['BidQty3']

        askqty1 = msg_dict['AskQty1']
        askqty2 = msg_dict['AskQty2']
        askqty3 = msg_dict['AskQty3']

        totalbidqty = msg_dict['TotalBidQty']
        totalaskqty = msg_dict['TotalAskQty']
        totalbidcnt = msg_dict['TotalBidCnt']
        totalaskcnt = msg_dict['TotalAskCnt']

        if 'Ask4' in msg_dict and 'Bid4' in msg_dict:
            bid4 = msg_dict['Bid4']
            bid5 = msg_dict['Bid5']
            ask4 = msg_dict['Ask4']
            ask5 = msg_dict['Ask5']
            bidqty4 = msg_dict['BidQty4']
            bidqty5 = msg_dict['BidQty5']
            askqty4 = msg_dict['AskQty4']
            askqty5 = msg_dict['AskQty5']

            bidcnt1 = msg_dict['BidCnt1']
            bidcnt2 = msg_dict['BidCnt2']
            bidcnt3 = msg_dict['BidCnt3']
            bidcnt4 = msg_dict['BidCnt4']
            bidcnt5 = msg_dict['BidCnt5']

            askcnt1 = msg_dict['AskCnt1']
            askcnt2 = msg_dict['AskCnt2']
            askcnt3 = msg_dict['AskCnt3']
            askcnt4 = msg_dict['AskCnt4']
            askcnt5 = msg_dict['AskCnt5']

            new_tickdata = TickData(shortcd=shortcd,
                                    feedsource=feedsource,
                                    taq=taq,
                                    securitiestype=securitiestype,
                                    datetime=timestamp,
                                    bid1=bid1,
                                    bid2=bid2,
                                    bid3=bid3,
                                    bid4=bid4,
                                    bid5=bid5,
                                    ask1=ask1,
                                    ask2=ask2,
                                    ask3=ask3,
                                    ask4=ask4,
                                    ask5=ask5,
                                    bidqty1=bidqty1,
                                    bidqty2=bidqty2,
                                    bidqty3=bidqty3,
                                    bidqty4=bidqty4,
                                    bidqty5=bidqty5,
                                    askqty1=askqty1,
                                    askqty2=askqty2,
                                    askqty3=askqty3,
                                    askqty4=askqty4,
                                    askqty5=askqty5,
                                    bidcnt1=bidcnt1,
                                    bidcnt2=bidcnt2,
                                    bidcnt3=bidcnt3,
                                    bidcnt4=bidcnt4,
                                    bidcnt5=bidcnt5,
                                    askcnt1=askcnt1,
                                    askcnt2=askcnt2,
                                    askcnt3=askcnt3,
                                    askcnt4=askcnt4,
                                    askcnt5=askcnt5,
                                    totalbidqty=totalbidqty,
                                    totalaskqty=totalaskqty,
                                    totalbidcnt=totalbidcnt,
                                    totalaskcnt=totalaskcnt,
                                    )

        else:
            new_tickdata = TickData(shortcd=shortcd,
                                    feedsource=feedsource,
                                    taq=taq,
                                    securitiestype=securitiestype,
                                    datetime=timestamp,
                                    bid1=bid1,
                                    bid2=bid2,
                                    bid3=bid3,
                                    ask1=ask1,
                                    ask2=ask2,
                                    ask3=ask3,
                                    bidqty1=bidqty1,
                                    bidqty2=bidqty2,
                                    bidqty3=bidqty3,
                                    askqty1=askqty1,
                                    askqty2=askqty2,
                                    askqty3=askqty3,
                                    totalbidqty=totalbidqty,
                                    totalaskqty=totalaskqty,
                                    totalbidcnt=totalbidcnt,
                                    totalaskcnt=totalaskcnt,
                                    )

    session.add(new_tickdata)
    session.commit()
    pass

if __name__ == '__main__':
    import datetime as dt
    import sqlalchemy_tickdata_init as tickdata_init

    session = tickdata_init.initSession('tickdata_test.db')[0]

    msg_dict = dict()
    msg_dict['ShortCD'] = '301LA207'
    msg_dict['FeedSource'] = 'xing'
    msg_dict['TAQ'] = 'Q'
    msg_dict['SecuritiesType'] = 'options'
    msg_dict['TimeStamp'] = dt.datetime.strptime('2016-09-07 03:39:24.145034', '%Y-%m-%d %H:%M:%S.%f')
    # msg_dict['TimeStamp'] = '2016-08-04 15:29:23.000506'
    msg_dict['Bid1'] = 0.01
    msg_dict['Ask1'] = 0.02
    msg_dict['BidQty1'] = 532
    msg_dict['AskQty1'] = 232

    for i in xrange(2, 4):
        msg_dict['Bid%d' % i] = 0.0
        msg_dict['Ask%d' % i] = 0.0
        msg_dict['BidQty%d' % i] = 0
        msg_dict['AskQty%d' % i] = 0

    msg_dict['TotalBidQty'] = 532
    msg_dict['TotalAskQty'] = 232
    msg_dict['TotalBidCnt'] = 0
    msg_dict['TotalAskCnt'] = 0

    # insertNewTickData(session, msg_dict)

    rows = session.query(TickData).limit(15)
    for row in rows:
        print (row.id, row.shortcd, row.datetime, row.taq, row.askqty1, row.ask1, row.bid1, row.bidqty1)
    pass
