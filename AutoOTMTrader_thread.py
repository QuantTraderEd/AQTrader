import zmq
from PyQt4 import QtCore

def cybos_convertor(strprice, floating):
    value = round(float(strprice), floating)
    strformat = '%.' + str(floating) + 'f'
    strValue = strformat%value
    return (strValue)
    
class OptionViewerThread(QtCore.QThread):
    receiveData = QtCore.pyqtSignal(str)

    def __init__(self,parent=None):
        QtCore.QThread.__init__(self,parent)
        self.msg = ''
        self.mt_stop = False
        self.mt_pause = False
        self.mutex = QtCore.QMutex()
        self.mt_pauseCondition = QtCore.QWaitCondition()        

    def run(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect("tcp://127.0.0.1:5500")
        self.socket.setsockopt(zmq.SUBSCRIBE,"")  
        
        while True:
            msg = self.socket.recv()
            self.receiveData.emit(msg)
            self.onReceiveData(msg)

            self.mutex.lock()
            if self.mt_stop: break
            self.mutex.unlock()
        pass

    def onReceiveData(self,msg):
        pass
    
    def stop(self):
        self.mt_stop = True
        pass


class ExecutionThread(QtCore.QThread):
    receiveData = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.msg = ''
        self.mt_stop = False
        self.mt_pause = False
        self.mutex = QtCore.QMutex()
        self.mt_pauseCondition = QtCore.QWaitCondition()

    def run(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        # self.socket.connect("ipc://127.0.0.1:6100")
        self.socket.connect("tcp://127.0.0.1:6100")
        self.socket.setsockopt(zmq.SUBSCRIBE, "")
        
        while True:
            data_dict = self.socket.recv_pyobj()
            self.receiveData.emit(data_dict)
            self.onReceiveData(data_dict)

            self.mutex.lock()
            if self.mt_stop: break
            self.mutex.unlock()
        pass

    def onReceiveData(self, data_dict):
        pass
    
    def stop(self):
        self.mt_stop = True
        pass