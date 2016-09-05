# -*- coding: utf-8 -*-

from datetime import datetime


class ZMQTickSender:
    count = 0

    def __init__(self, ZMQSocket=None, feedsource=None, feedtype=None, securitiestype=None):
        self.ZMQSocket = ZMQSocket
        self.feedsource = feedsource
        self.feedtype = feedtype
        self.securitiestype = securitiestype
        pass

    def Update(self,subject):
        dt = datetime.now()
        timestamp = datetime.strftime(dt,"%H:%M:%S.%f")[:-3]        
        msg = ''
        msg = msg + self.feedsource
        msg = msg + ',' + self.feedtype
        msg = msg + ',' + self.securitiestype
        for i in xrange(len(subject.data)):
            msg = msg + ',' +  str(subject.data[i])
        msg = timestamp + ',' + msg        
        self.ZMQSocket.send(msg)
        if self.securitiestype in ['futures', 'options']:
            ZMQTickSender.count += 1
        pass


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
        timestamp = datetime.strftime(now_dt,"%H:%M:%S.%f")[:-3]        
        
        msg_dict = {}
        
        msg_dict['ShortCD'] = shortcd
        msg_dict['FeedSource'] = self.feedsource
        msg_dict['TAQ'] = self.taq
        msg_dict['SecuritiesType'] = self.securitiestype
        msg_dict['TimeStamp'] = timestamp
        
        if self.taq == 'T' and self.securitiestype in ['futures', 'options']:
            msg_dict['LastPrice'] = subject.data['LastPrice']
            msg_dict['LastQty'] = subject.data['LastQty']
            if subject.data['BuySell'] == '+':
                msg_dict['BuySell'] = 'B'
            elif subject.data['BuySell'] == '-':
                msg_dict['BuySell'] = 'S'
            else:
                msg_dict['BuySell'] = ''
            msg_dict['Ask1'] = subject.data['Ask1']
            msg_dict['Bid1'] = subject.data['Bid1']
            
        elif self.taq == 'Q' and self.securitiestype in ['futures', 'options']:
            msg_dict['Ask1'] = subject.data['Ask1']
            msg_dict['Bid1'] = subject.data['Bid1']
            msg_dict['AskQty1'] = subject.data['AskQty1']
            msg_dict['BidQty1'] = subject.data['BidQty1']
            msg_dict['Ask2'] = subject.data['Ask2']
            msg_dict['Bid2'] = subject.data['Bid2']
            msg_dict['AskQty2'] = subject.data['AskQty2']
            msg_dict['BidQty2'] = subject.data['BidQty2']
            msg_dict['Ask3'] = subject.data['Ask3']
            msg_dict['Bid3'] = subject.data['Bid3']
            msg_dict['AskQty3'] = subject.data['AskQty3']
            msg_dict['BidQty3'] = subject.data['BidQty3']
            if 'Ask4' in subject.data and 'Bid4' in subject.data:
                msg_dict['Ask4'] = subject.data['Ask4']
                msg_dict['Bid4'] = subject.data['Bid4']
                msg_dict['AskQty4'] = subject.data['AskQty4']
                msg_dict['BidQty4'] = subject.data['BidQty4']
                msg_dict['Ask5'] = subject.data['Ask5']
                msg_dict['Bid5'] = subject.data['Bid5']
                msg_dict['AskQty5'] = subject.data['AskQty5']
                msg_dict['BidQty5'] = subject.data['BidQty5']

            msg_dict['TotalAskQty'] = subject.data['TotalAskQty']
            msg_dict['TotalBidQty'] = subject.data['TotalBidQty']
            msg_dict['TotalAskCnt'] = subject.data['TotalAskCnt']
            msg_dict['TotalBidCnt'] = subject.data['TotalBidCnt']
        elif self.taq == 'E' and self.securitiestype in ['futures', 'options']:
            msg_dict['ExpectPrice'] = subject.data['ExpectPrice']
        else:
            return

        self.zmq_socket.send_pyobj(msg_dict)
        if self.securitiestype in ['futures', 'options']:
            ZMQTickSender.count += 1
        pass
