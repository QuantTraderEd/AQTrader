# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler

from DataLoader.dataloader.SubscribeReceiverThread import SubscribeThread

logger = logging.getLogger('SubExample')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('SubExample.log')
fh = RotatingFileHandler('SubExample.log', maxBytes=5242, backupCount=3)
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

    def onReceiveData(self, msg_dict):
        logger.info("recv data: %s" % msg_dict)


def main():
    sub_thread = RecvThread(port=5510)
    sub_thread.run()


if __name__ == "__main__":
    main()
