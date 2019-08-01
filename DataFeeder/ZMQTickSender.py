# -*- coding: utf-8 -*-

from datetime import datetime


# class ZMQTickSender:
#     count = 0
#
#     def __init__(self, ZMQSocket=None, feedsource=None, feedtype=None, securitiestype=None):
#         self.ZMQSocket = ZMQSocket
#         self.feedsource = feedsource
#         self.feedtype = feedtype
#         self.securitiestype = securitiestype
#         pass
#
#     def Update(self,subject):
#         dt = datetime.now()
#         timestamp = datetime.strftime(dt,"%H:%M:%S.%f")[:-3]
#         msg = ''
#         msg = msg + self.feedsource
#         msg = msg + ',' + self.feedtype
#         msg = msg + ',' + self.securitiestype
#         for i in xrange(len(subject.data)):
#             msg = msg + ',' +  str(subject.data[i])
#         msg = timestamp + ',' + msg
#         self.ZMQSocket.send(msg)
#         if self.securitiestype in ['futures', 'options']:
#             ZMQTickSender.count += 1
#         pass


class ZMQTickSender_New:
    count = 0

    def __init__(self, zmq_socket=None, feedsource=None, taq=None, securitiestype=None):
        self.zmq_socket = zmq_socket
        self.feedsource = feedsource
        self.taq = taq
        self.securitiestype = securitiestype
        pass
    
    def Update(self,subject):        
        if type(subject.data) != dict: return
        shortcd = subject.data['ShortCD']
        now_dt = datetime.now()
        # timestamp = datetime.strftime(now_dt,"%H:%M:%S.%f")[:-3]
        
        msg_dict = {}
        
        msg_dict['ShortCD'] = shortcd
        msg_dict['FeedSource'] = self.feedsource
        msg_dict['TAQ'] = self.taq
        msg_dict['SecuritiesType'] = self.securitiestype
        if shortcd[:3] == '105':
            self.securitiestype = 'futures'
            msg_dict['SecuritiesType'] = self.securitiestype
        msg_dict['TimeStamp'] = now_dt
        
        if self.taq == 'T' and self.securitiestype in ['futures', 'options']:
            msg_dict['LastPrice'] = float(subject.data['LastPrice'])
            msg_dict['LastQty'] = int(subject.data['LastQty'])
            if subject.data['BuySell'] == '+':      # xing api
                msg_dict['BuySell'] = 'B'
            elif subject.data['BuySell'] == '-':    # xing api
                msg_dict['BuySell'] = 'S'
            else:
                msg_dict['BuySell'] = ''
            msg_dict['Ask1'] = float(subject.data['Ask1'])
            msg_dict['Bid1'] = float(subject.data['Bid1'])
            
        elif self.taq == 'Q' and self.securitiestype in ['futures', 'options']:
            for i in xrange(1, 4):
                msg_dict['Ask%d' % i] = float(subject.data['Ask%d' % i])
                msg_dict['Bid%d' % i] = float(subject.data['Bid%d' % i])
                msg_dict['AskQty%d' % i] = int(subject.data['AskQty%d' % i])
                msg_dict['BidQty%d' % i] = int(subject.data['BidQty%d' % i])

            if 'Ask4' in subject.data and 'Bid4' in subject.data:
                for i in xrange(4, 6):
                    msg_dict['Ask%d' % i] = float(subject.data['Ask%d' % i])
                    msg_dict['Bid%d' % i] = float(subject.data['Bid%d' % i])
                    msg_dict['AskQty%d' % i] = int(subject.data['AskQty%d' % i])
                    msg_dict['BidQty%d' % i] = int(subject.data['BidQty%d' % i])

            if 'AskCnt4' in subject.data and 'BidCnt4' in subject.data:
                for i in xrange(1, 6):
                    msg_dict['AskCnt%d' % i] = int(subject.data['AskCnt%d' % i])
                    msg_dict['BidCnt%d' % i] = int(subject.data['BidCnt%d' % i])

            msg_dict['TotalAskQty'] = int(subject.data['TotalAskQty'])
            msg_dict['TotalBidQty'] = int(subject.data['TotalBidQty'])
            msg_dict['TotalAskCnt'] = int(subject.data['TotalAskCnt'])
            msg_dict['TotalBidCnt'] = int(subject.data['TotalBidCnt'])

        elif self.taq == 'E' and self.securitiestype in ['futures', 'options']:
            msg_dict['ExpectPrice'] = float(subject.data['ExpectPrice'])
        else:
            return

        self.zmq_socket.send_pyobj(msg_dict)
        if self.securitiestype in ['futures', 'options']:
            ZMQTickSender_New.count += 1
        pass
