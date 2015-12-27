# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 07:52:42 2013

@author: Administrator
"""


from datetime import datetime

class ZMQTickSender:
    count = 0
    def __init__(self,ZMQSocket=None,FeedSource=None,FeedType=None,SecuritiesType=None):
        self.ZMQSocket = ZMQSocket
        self.FeedSource = FeedSource
        self.FeedType = FeedType
        self.SecuritiesType = SecuritiesType
        pass
    def Update(self,subject):
        dt = datetime.now()
        timestamp = datetime.strftime(dt,"%H:%M:%S.%f")[:-3]        
        msg = ''
        msg = msg + self.FeedSource 
        msg = msg + ',' + self.FeedType
        msg = msg + ',' + self.SecuritiesType
        for i in xrange(len(subject.data)):
            msg = msg + ',' +  str(subject.data[i])
        msg = timestamp + ',' + msg        
        self.ZMQSocket.send(msg)
        if self.SecuritiesType in ['futures', 'options']:
            self.count += 1
        pass
class ZMQTickSender_New:
    count = 0
    def __init__(self,ZMQSocket=None,FeedSource=None,TAQ=None,SecuritiesType=None):
        self.ZMQSocket = ZMQSocket
        self.FeedSource = FeedSource
        self.TAQ = TAQ
        self.SecuritiesType = SecuritiesType
        pass
    
    def Update(self,subject):
        if type(subject.data) != dict: return
        shortcd = subject.data['shortcd']
        now_dt = datetime.now()
        timestamp = datetime.strftime(now_dt,"%H:%M:%S.%f")[:-3]        
        
        msg_dict = {}
        
        msg_dict['ShortCD'] = shortcd
        msg_dict['FeedSource'] = self.FeedSource
        msg_dict['TAQ'] = self.TAQ
        msg_dict['SecuritiesType'] = self.SecuritiesType
        msg_dict['Time'] = timestamp
        
        if self.TAQ == 'T' and self.SecuritiesType in ['futures', 'options']:
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
        elif self.TAQ == 'Q' and self.SecuritiesType in ['futures', 'options']:
            msg_dict['Ask1'] = subject.data['Ask1']
            msg_dict['Bid1'] = subject.data['Bid1']
            msg_dict['Askqty1'] = subject.data['Askqty1']
            msg_dict['Bidqty1'] = subject.data['Bidqty1']
            msg_dict['Ask2'] = subject.data['Ask2']
            msg_dict['Bid2'] = subject.data['Bid2']
            msg_dict['Askqty2'] = subject.data['Askqty2']
            msg_dict['Bidqty2'] = subject.data['Bidqty2']
            msg_dict['Ask3'] = subject.data['Ask3']
            msg_dict['Bid3'] = subject.data['Bid3']
            msg_dict['Askqty3'] = subject.data['Askqty3']
            msg_dict['Bidqty3'] = subject.data['Bidqty3']
            
            msg_dict['TotalAskQty'] = subject.data['TotalAskQty']
            msg_dict['TotalBidQty'] = subject.data['TotalBidQty']
            msg_dict['TotalAskCnt'] = subject.data['TotalAskCnt']
            msg_dict['TotalBidCnt'] = subject.data['TotalBidCnt']
            
        
#        for i in xrange(len(subject.data)):
#            msg = msg + ',' +  str(subject.data[i])
            
        
        #self.ZMQSocket.send(msg)
        self.ZMQSocket.send_pyobj(msg_dict)
        if self.SecuritiesType in ['futures', 'options']:
            ZMQTickSender.count += 1
        pass
