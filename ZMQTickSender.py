# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 07:52:42 2013

@author: Administrator
"""


from datetime import datetime

class ZMQTickSender:
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
        msglist = []
        msglist.append(self.FeedSource)
        msglist.append(self.FeedType)
        msglist.append(self.SecuritiesType)        
        for i in xrange(len(subject.data)):
            msglist.append(str(subject.data[i]))
        
        msg = ",".join(msglist)
        msg = timestamp + ',' + msg        
        self.ZMQSocket.send(msg)       
        pass