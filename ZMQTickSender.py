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
        self.count += 1
        pass
