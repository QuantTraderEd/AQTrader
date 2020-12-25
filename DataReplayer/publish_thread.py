# -*- coding: utf-8 -*-

import time
import logging
import zmq
import datetime as dt
import sqlite3 as lite
import pandas as pd
from PyQt4 import QtCore

from DataFeeder.ZMQTickSender import ZMQTickSenderReplay
from DataLoader.dataloader.sqlalchemy_tickdata_init import TickData, init_session


class PublishThread(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.logger = logging.getLogger('DataReplayer.PubThread')
        self.pub_port = 5510
        self.timesleep_multiple = 1
        self.mt_stop = False
        self.mt_pause = False
        self.mutex = QtCore.QMutex()
        self.mt_pause_condition = QtCore.QWaitCondition()
        self.zmq_tick_sender = ZMQTickSenderReplay()
        self.logger.info('Init Thread')

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
        -- LIMIT 100
        """
        self.data = pd.read_sql(sqltext, conn)
        self.data['datetime'] = pd.to_datetime(self.data['datetime'])
        # session, engine = init_session(db_name)
        # self.data = engine.execute(sqltext)

    def run(self):
        self.init_zmq()
        self.init_data()

        prev_datetime = self.data.iloc[0]['datetime']

        time.sleep(4)
        self.logger.info("start publish data....")

        for i in range(len(self.data)):
            row = self.data.iloc[i]

            msg_dict = dict(row)
            now_datetime = msg_dict['datetime']
            now_td = now_datetime - prev_datetime
            time.sleep((now_td.seconds + now_td.microseconds * 0.000001) / self.timesleep_multiple)
            prev_datetime = now_datetime
            self.socket.send_pyobj(msg_dict)
            msg = "%s %s %.2f %.2f" % (msg_dict['datetime'], msg_dict['shortcd'], msg_dict['bid1'], msg_dict['ask1'])
            self.logger.info("%s" % msg)
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
