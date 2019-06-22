# -*- coding: utf-8 -*-

import win32com
import win32com.client
import pythoncom
from pythoncom import CoInitialize
from win32com.client import gencache, DispatchWithEvents, Dispatch


# self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl1.1")
# ret = self.kiwoom.dynamicCall("CommConnect()")

class KHOPENAPI_Events:
    def OnEventConnect(self, *args):
        print "OnEventConnect", args

gencache.EnsureModule("A1574A0D-6BFA-4BD7-9020-DED88711818D", 0, 1, 0)
gencache.EnsureModule("CF20FBB6-EDD4-4BE5-A473-FEF91977DEB6", 0, 1, 0)
gencache.EnsureModule("7335F12D-8973-4BD5-B7F0-12DF03D175B7", 0, 1, 0)
gencache.EnsureModule("6D8C2B4D-EF41-4750-8AD4-C299033833FB", 0, 1, 0)

kiwoom = win32com.client.DispatchWithEvents("KHOPENAPI.KHOpenAPICtrl.1", KHOPENAPI_Events)
ret = kiwoom.CommConnect()
print ret
# kiwoom.GetConnectState()

while True:
    pythoncom.PumpWaitingMessages() 

# print text.decode('cp949').encode('utf-8')
# 오류입니다.
