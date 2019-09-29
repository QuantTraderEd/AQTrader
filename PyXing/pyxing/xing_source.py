# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 19:53:49 2013

@author: Administrator
"""
from weakref import proxy
from pythoncom import CoInitialize
from win32com.client import DispatchWithEvents


class XASessionEvents:
    def OnLogin(self,szCode,szMsg):
        self.parent.OnLogin(szCode,szMsg)
        self.parent.flag = False
        
    def OnLogout(self, *args):
        self.parent.OnLogout(args)
        
    def OnDisconnect(self, *args):
        self.parent.OnDisconnect(args)
        
class XAQueryEvents:
    def OnReceiveData(self, *args):
        self.parent.OnSignal()
        pass
    def OnReceiveMessage(self,blsSystemError,szMessageCode,szMessage):        
        self.parent.RecvMsg = [blsSystemError,szMessageCode,szMessage]        
        pass
        
class XARealEvents:
    def OnReceiveRealData(self, *args):
        self.parent.OnSignal()
        pass
    


class XASession(object):
    def __init__(self):
        self.event  = DispatchWithEvents("XA_Session.XASession", XASessionEvents)
        self.com    = self.event._obj_
        self.event.parent = proxy(self)
        self.observer = None
        self.observers = []        
        self.data = None
        self.flag = False                
        pass
    
    # Method
    
    def ConnectServer(self,server,port):
        self.event.ConnectServer(server,port)
    def DisconnectServer(self):
        self.com.DisconnectServer()
        pass
    def IsConnected(self):
        return self.com.IsConnected()
        pass
    def Login(self,user,password,certpw,servertype,showcerterror):
        self.event.Login(user,password,certpw,servertype,showcerterror)
        self.flag = True
        pass
    def Logout(self):
        pass
    def GetAccountListCount(self):
        if self.IsConnected():
            return self.com.GetAccountListCount()
        else:
            return 0
    def GetAccountList(self):
        if self.IsConnected():
            accountlist = []
            for item in range(self.GetAccountListCount()):
                accountlist.append(self.com.GetAccountList(item))
            return accountlist        
        else:
            return 0
    def GetLastError(self):
        nErrorCode = self.com.GetLastError()
        return nErrorCode
    def GetErrorMessage(self,nErrorCode):
        szErrorMessage = self.com.GetErrorMessage(nErrorCode)
        return szErrorMessage
    def IsLoadAPI(self):
        return self.com.IsLoadAPI()
    def GetServerName(self):
        return self.com.GetServerName()
    
    # Event
    
    def OnLogin(self,szCode,szMsg):
        #self.data = [szCode,szMsg]
        self.data = [szCode]
        self.flag = False
        self.Notify()
    def OnLogout(self,args):
        self.data = [args]
        self.Notify()
    def OnDisconnect(self, *args):
        self.data = [args]
        self.Notify()
        # need to alert disconnect
        
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
    def Notify(self):
        if self.observer != None: self.observer.update(proxy(self))
        for observer in self.observers:
            observer.update(proxy(self))
        pass
    def OnSignal(self):
        raise NotImplementedError

class SourceQuery(object):
    def __init__(self,com_module):
        self.event = DispatchWithEvents(com_module,XAQueryEvents)
        self.com = self.event._obj_
        self.event.parent = proxy(self)
        self.RecvMsg = []
        self.observer = None
        self.observers = []
        pass
    
    # observer routine
    
    # Method
    
    def Request(self,bNext=False):
        self.com.Request(bNext)
        # need to error rutine        
    def GetFieldData(self,szBlockName,szFieldName,nOccur=-1):
        if nOccur == -1:
            return self.com.GetFieldData(szBlockName,szFieldName)
        else:
            return self.com.GetFieldData(szBlockName,szFieldName,nOccur)
        pass
    def SetFieldData(self,szBlockName,szFieldName = '',nOccur=0,szData=''):                
        self.com.SetFieldData(szBlockName,szFieldName,nOccur,szData)
        pass
    def GetBlockCount(self,szBlockName):
        num = self.com.GetBlockCount(szBlockName)
        return num
    def SetBlockCount(self,szBlockName,nCount):
        self.com.SetBlockCount(szBlockName,nCount)        
    def LoadFromResFile(self,filepathname):
        self.com.LoadFromResFile(filepathname)
        #need to error rutine
        pass
    def ClearBlockData(self,szBlockName):
        self.com.ClearBlockData(szBlockName)
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
    def Notify(self):        
        if self.observer != None: self.observer.update(proxy(self))
        for observer in self.observers:
            observer.update(proxy(self))
        pass
    def OnSignal(self):        
        raise NotImplementedError
    

class SourceReal(object):
    def __init__(self,com_module):
        self.event = DispatchWithEvents(com_module, XARealEvents)        
        self.com    = self.event._obj_
        self.event.parent = proxy(self)
        self.observer = None
        self.observers = []
        self.RecvMsg = None
        pass
    
    # method
    def AdviseRealData(self):
        self.com.AdviseRealData()
        CoInitialize()
        pass
    def UnAdviseRealData(self):
        self.com.UnAdviseRealData()
        pass
    def UnAdviseRealDataWithKey(self,szCode):
        self.com.UnAdviseRealDataWithKey(szCode)
        pass
    def GetFieldData(self,szBlockName,szFieldName,nOccur=-1):
        if nOccur == -1:
            return self.com.GetFieldData(szBlockName,szFieldName)
        else:
            return self.com.GetFieldData(szBlockName,szFieldName,nOccur)            
        pass
    def SetFieldData(self,szBlockName,szFieldName,szData):        
        self.com.SetFieldData(szBlockName,szFieldName,szData)
        pass
    def LoadFromResFile(self,filepathname):
        self.com.LoadFromResFile(filepathname)
        # need to error rutine
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
        
    def Notify(self):
        if self.observer != None: self.observer.update(proxy(self))
        for observer in self.observers:
            observer.update(proxy(self))
        pass
    def OnSignal(self):
        raise NotImplementedError