# -*- coding: utf-8 -*-

import time
import logging
import zmq
import sqlite3 as lite
import pandas as pd
from PyQt4 import QtCore

from DataFeeder.ZMQTickSender import ZMQTickSenderReplay
from DataLoader.dataloader.sqlalchemy_tickdata_init import TickData, init_session


class PublishThread(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.logger = logging.getLogger('DataReplayer.Thread')
        self.pub_port = 5510
        self.mt_stop = False
        self.mt_pause = False
        self.mutex = QtCore.QMutex()
        self.mt_pause_condition = QtCore.QWaitCondition()
        self.zmq_tick_sender = ZMQTickSenderReplay()

    def init_zmq(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://127.0.0.1:%d" % self.pub_port)
        self.zmq_tick_sender.zmq_socket = self.socket

    def init_data(self):
        db_name = '../DataLoader/TAQ_Data/TAQ_20200518.db'
        # self.session = init_session(db_name)[0]
        conn = lite.connect(db_name)
        sqltext = """
        SELECT * 
        From TickData 
        WHERE
        securitiestype = 'futures'
        AND datetime >= '2020-05-18 09:00:00'
        LIMIT 10
        """
        self.data = pd.read_sql(sqltext, conn)

    def run(self):
        self.init_zmq()
        self.init_data()

        # rows = self.session.query(TickData).filter_by(TickData.datetime.hour >= 9).limit(20)

        for i in range(10):
            time.sleep(1)
            row = self.data.iloc[i]
            msg_dict = dict(row)
            self.socket.send_pyobj(msg_dict)
            self.logger.info("%s" % msg_dict)
            self.mutex.lock()
            if self.mt_stop:
                break
            if self.mt_pause:
                self.mt_pauseCondition.wait(self.mutex)
            self.mutex.unlock()

    def mtf_stop(self):
        self.mt_stop = True

    def mtf_pause(self):
        self.mt_pause = True

    def mtf_resume(self):
        self.mt_pause = False
        self.mt_pause_condition.wakeAll()

    def mtf_reset(self):
        self.mt_stop = False
        self.mt_pause = False
        self.mutex.unlock()
