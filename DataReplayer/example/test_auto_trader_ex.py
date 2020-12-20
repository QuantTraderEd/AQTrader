# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler

from DataLoader.dataloader.SubscribeReceiverThread import SubscribeThread

logger = logging.getLogger('Test_AutoTrader')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('Test_AutoTrader.log')
fh = RotatingFileHandler('Test_AutoTrader.log', maxBytes=5242, backupCount=1)
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handler to logger
logger.addHandler(fh)
logger.addHandler(ch)


class RecvThread(SubscribeThread):
    def __init__(self, parent=None, port=5503):
        SubscribeThread.__init__(self, parent, port)
        self.big_mid = 0
        self.mini_mid = 0
        self.big_mini_spread = 0

    def onReceiveData(self, msg_dict):
        # logger.info("recv data: %s" % msg_dict)
        if msg_dict['securitiestype'] != u'futures': return

        mid_price = (msg_dict['bid1'] + msg_dict['ask1']) * 0.5
        if msg_dict['shortcd'][:3] == '101':
            self.big_mid = mid_price
        elif msg_dict['shortcd'][:3] == '105':
            self.mini_mid = mid_price

        if self.big_mid > 0 and self.mini_mid > 0:
            big_mini_spread = self.big_mid - self.mini_mid
            msg = "%s %.3f %.3f %.3f" % (msg_dict['datetime'], self.big_mid, self.mini_mid, big_mini_spread)
            logger.info("%s" % msg)


def main():
    sub_thread = RecvThread(port=5510)
    sub_thread.run()


if __name__ == "__main__":
    main()