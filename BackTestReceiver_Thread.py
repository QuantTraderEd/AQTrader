# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 10:27:17 2014

@author: assa
"""

import pdb
import zmq
import datetime
import numpy as np
import pandas as pd
import BlackSholesPricer as pricer

from PyQt4 import QtCore


def cybos_convertor(strprice, floating):
    value = round(float(strprice), floating)
    strformat = '%.' + str(floating) + 'f'
    strValue = strformat%value
    return (strValue)
    
def convert_strike(strike):
    if type(strike).__name__ == 'unicode':
        if strike[2] == '2' or strike[2] == '7':
            return '%s.5'%strike
        else:
            return strike
pass

def convert_df_strike(x):
    if x['Strike'] % 5 == 2:
        return x['Strike'] + 0.5
    else:
        return x['Strike']
    
class BackTestReceiverThread(QtCore.QThread):
    receiveData = QtCore.pyqtSignal(dict)
    updateImVol = QtCore.pyqtSignal(pd.DataFrame)
    def __init__(self,parent=None):
        QtCore.QThread.__init__(self,parent)
        self.msg = ''
        self.mt_stop = False
        self.mt_pause = False
        self.mutex = QtCore.QMutex()
        self.mt_pauseCondition = QtCore.QWaitCondition()       
        
        self.df_mid = pd.DataFrame(columns=('Time', 'ShortCD', 'Ask1', 'Bid1')) 
        self.df_imvol = pd.DataFrame(columns=('Time', 'ShortCD', 'Strike','Ask1', 'Bid1', 'ImVol')) 
        self.df_call_imvol = pd.DataFrame(columns=('Time', 'ShortCD', 'Strike', 'Ask1', 'Bid1', 'ImVol')) 
        self.df_put_imvol = pd.DataFrame(columns=('Time', 'ShortCD', 'Strike', 'Ask1', 'Bid1', 'ImVol')) 
        self.r = 0.0
        self.isGETATM = False
        
    def run(self):
        self.mt_stop = False               
        self.mt_pause = False
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect("tcp://127.0.0.1:5501")
        self.socket.setsockopt(zmq.SUBSCRIBE,"")           
        
        while True:
            row = self.socket.recv_pyobj()
            self.receiveData.emit(row)
            self.onReceiveData(row)

            self.mutex.lock()
            if self.mt_stop: break
            self.mutex.unlock()
        pass
    
    def stop(self):
        self.mt_stop = True
        pass

    def onReceiveData(self,row): 
        if row['TAQ'] != 'Q':
            return
        if row['ShortCD'][3:5] == 'K3' and float(row['Ask1']) and float(row['Bid1']):
            print row['Time'], row['ShortCD'], row['Ask1'], row['Bid1'], (float(row['Ask1']) + float(row['Bid1'])) * 0.5
            item = [row['Time'], row['ShortCD'], row['Ask1'], row['Bid1']]           
            
            if not row['ShortCD'] in list(self.df_mid['ShortCD']):        
                self.mutex.lock()
                self.df_mid.loc[len(self.df_mid)] = item
                self.mutex.unlock()
            else:
                index = self.df_mid[self.df_mid['ShortCD'] == row['ShortCD']].index[0]
                self.mutex.lock()
                self.df_mid.ix[index] = item
                self.mutex.unlock()
            
            self.df_mid = self.df_mid.sort('ShortCD')
            self.df_mid = self.df_mid[abs(self.df_mid['Ask1'].astype(float) - self.df_mid['Bid1'].astype(float)) < 0.3]
            #print self.df_mid
            self.get_atm()
                        
            if not (self.isGETATM and row['ShortCD'] in list(self.df_mid['ShortCD'])) : return   
            
            self.T = 6.25 * 9 + 11 * 8 - self.get_Time(row['Time'])            
            S0 = self.call_atm_price - self.put_atm_price + self.atm_strike
            K = float(row['ShortCD'][-3:])
            if K % 5: K += 0.5
            OptionType = ''
            if row['ShortCD'][0] == '2': OptionType = 'C'
            elif row['ShortCD'][0] == '3': OptionType = 'P'
            else:
                return            
            midprice = (float(row['Ask1']) + float(row['Bid1'])) * 0.5            
            Vol = 0.0017
            imvol = pricer.CalcImpliedVolatility(OptionType, S0, K, self.r, self.T, midprice, 0.000001, Vol)            
            incre = -0.0001
            count = 0
            
            while np.isnan(imvol):                
                count += 1                
                Vol += incre * -1.0
                incre = cmp(incre,0) * abs(incre) * 2
                imvol = pricer.CalcImpliedVolatility(OptionType, S0, K, self.r, self.T, midprice, 0.000001, Vol)
                if count > 4: 
                    break
                
            print row['Time'], row['ShortCD'], row['Ask1'], row['Bid1'], imvol            
            
            imvol = '%.8f'%imvol
            item = [row['Time'], row['ShortCD'], str(K), row['Ask1'], row['Bid1'] ,imvol]
            
            
            if not row['ShortCD'] in list(self.df_imvol['ShortCD']):        
                self.mutex.lock()
                self.df_imvol.loc[len(self.df_imvol)] = item
                self.mutex.unlock()
            else:
                index = self.df_imvol[self.df_imvol['ShortCD'] == row['ShortCD']].index[0]
                self.mutex.lock()
                self.df_imvol.ix[index] = item
                self.mutex.unlock()
            
            self.df_imvol = self.df_imvol.sort('ShortCD')            
            #print self.df_imvol
            self.updateImVol.emit(self.get_volsurf(self.df_imvol))
            
        pass
    
    def get_Time(self,strTime):
        starttime = datetime.datetime(1900, 1, 1, 9, 0, 0)
        nowtime = datetime.datetime.strptime(strTime,'%H:%M:%S.%f')
        td = nowtime - starttime
        return td.seconds / 3600.0
        
    
    def get_atm(self):        
        df_mid = self.df_mid.copy()
        df_mid['Strike'] = df_mid['ShortCD'].str[-3:]
        df_mid['Strike'] = df_mid['Strike'].astype(float)        
        if len(df_mid) > 0:            
            #df_mid['Strike'] = df_mid.apply(convert_df_strike,axis=1) # need time test
            df_mid.ix[df_mid['Strike'] % 5 != 0,'Strike'] = df_mid.ix[df_mid['Strike'] % 5 != 0,'Strike'] + 0.5
        
        df_call_mid = df_mid[df_mid['ShortCD'].str[:3] == '201']
        df_put_mid = df_mid[df_mid['ShortCD'].str[:3] == '301']
        
        if len(df_call_mid) < 5 or len(df_put_mid) <  5:
            return
                    
                    
        df_call_mid['Mid'] = (df_call_mid['Bid1'].astype(float) + df_call_mid['Ask1'].astype(float)) * 0.5
        df_put_mid['Mid'] = (df_put_mid['Bid1'].astype(float) + df_put_mid['Ask1'].astype(float)) * 0.5
        
        df_syth = df_call_mid.merge(df_put_mid,left_on='Strike',right_on='Strike',how='outer')
        df_syth['SythPrice'] = df_syth['Mid_x'].astype(float) - df_syth['Mid_y'].astype(float) + df_syth['Strike'].astype(float)
        
        df_syth['Differ'] = abs(df_syth['Mid_x'].astype(float) - df_syth['Mid_y'].astype(float))
        df_syth = df_syth.sort('Differ')
        
        self.call_atm_price = df_syth.iloc[0]['Mid_x']
        self.put_atm_price = df_syth.iloc[0]['Mid_y']
        self.atm_strike = float(df_syth.iloc[0]['Strike'])        
        
        print self.atm_strike, self.call_atm_price, self.put_atm_price
        if self.call_atm_price and not np.isnan(self.put_atm_price): self.isGETATM = True
        pass
    
    def get_volsurf(self, df_imvol):        
        df_call_imvol = df_imvol[(df_imvol['ShortCD'].str[0] == '2') & (df_imvol['Strike'].astype(float) >= self.atm_strike)]    
        df_put_imvol = df_imvol[(df_imvol['ShortCD'].str[0] == '3') & (df_imvol['Strike'].astype(float) <= self.atm_strike)]    
        df = df_call_imvol.append(df_put_imvol)
        df = df.sort('Strike')         
        return df
        pass
        
