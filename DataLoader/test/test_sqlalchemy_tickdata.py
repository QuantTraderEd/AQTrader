# -*- coding: utf-8 -*-

import datetime as dt
import AQTrader.DataLoader.dataloader.sqlalchemy_tickdata_declarative as tickdata_declare
import AQTrader.DataLoader.dataloader.sqlalchemy_tickdata_init as tickdata_init
import AQTrader.DataLoader.dataloader.sqlalchemy_tickdata_insert as tickdata_insert


class TestClass(object):
    session = tickdata_init.init_session('tickdata_test.db')[0]

    def test_tickdata_insert(self):
        shortcd = '301NC207'
        now_dt = dt.datetime.now()
        msg_dict = dict()
        msg_dict['ShortCD'] = shortcd
        msg_dict['FeedSource'] = 'xing'
        msg_dict['TAQ'] = 'Q'
        msg_dict['SecuritiesType'] = 'options'
        msg_dict['TimeStamp'] = now_dt
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

        tickdata_insert.insert_new_tickdata(self.session, msg_dict)

        rows = self.session.query(tickdata_declare.TickData).filter(tickdata_declare.TickData.shortcd == shortcd)\
                                                            .filter(tickdata_declare.TickData.datetime == now_dt)\
                                                            .all()
        assert len(rows) == 1
        assert rows[0].shortcd == shortcd
        assert rows[0].datetime == now_dt
