# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 12:58:49 2013

@author: Administrator
"""

from weakref import proxy
from pythoncom import CoInitialize
from win32com.client import gencache, DispatchWithEvents, Dispatch



class CpEvent(object):
    def OnReceived(self):
        self.parent.OnSignal()
        pass
    def OnDisConnect(self):
        """ CpUtil.CpCybos.1 에서 사용됨 """
        self.parent.OnDisConnect()
    pass

class Source(object):
    def __init__(self, com_module):
        gencache.EnsureModule("859343F1-08FD-11D4-8231-00105A7C4F8C", 0, 1, 0)
        gencache.EnsureModule("9C31B76A-7189-49A3-9781-3C6DD6ED5AD3", 0, 1, 0)
        gencache.EnsureModule("1F7D5E5A-05AB-4236-B6F3-3D383B09203A", 0, 1, 0)
        gencache.EnsureModule("2DA9C35C-FE59-4A32-A942-325EE8A6F659", 0, 1, 0)
        self.event  = DispatchWithEvents(com_module, CpEvent)
        self.com    = self.event._obj_
        self.event.parent = proxy(self)
        self.observers = []
        pass
    # observer routine
    def Attach(self, obs):
        if not obs in self.observers:
            self.observers.append(obs)
        pass
    def Detach(self, obs):
        try:
            self.observers.remove(obs)
        except ValueError:
            pass
        pass
    def SetInputValue(self, _type, code):
        self.com.SetInputValue(_type, code)
        pass
    def GetHeaderValue(self, _type):
        return self.com.GetHeaderValue(_type)
    def GetDataValue(self, _type, index):
        return self.com.GetDataValue(_type, index)
    def Request(self):
        self.com.Request()
        pass
    def BlockRequest(self):
        return self.com.BlockRequest()
    def Subscribe(self, _type = None, code = None):
        if _type and code : self.SetInputValue(_type, code)
        self.com.SubscribeLatest()
        CoInitialize()
        pass
    def Unsubscribe(self):
        self.com.Unsubscribe()
        pass
    def Notify(self):
        for obs in self.observers:
            obs.update(proxy(self))
            pass
        pass
    def OnSignal(self):
        raise NotImplementedError
    def OnDisConnect(self): # For CpUtil.CpCybos
        raise NotImplementedError

class SourceNoEvent(object):
    def __init__(self, com_module):
        gencache.EnsureModule("859343F1-08FD-11D4-8231-00105A7C4F8C", 0, 1, 0)
        gencache.EnsureModule("9C31B76A-7189-49A3-9781-3C6DD6ED5AD3", 0, 1, 0)
        gencache.EnsureModule("1F7D5E5A-05AB-4236-B6F3-3D383B09203A", 0, 1, 0)
        gencache.EnsureModule("2DA9C35C-FE59-4A32-A942-325EE8A6F659", 0, 1, 0)
        self.com    = Dispatch(com_module)