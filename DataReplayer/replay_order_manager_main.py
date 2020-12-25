# -*- coding: utf-8 -*-

import logging
import sqlite3
import pandas as pd

from logging.handlers import RotatingFileHandler

from reply_thread import ReplyThread

logger = logging.getLogger('replay_order_manager')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('replay_order_manager.log')
fh = RotatingFileHandler('replay_order_manager.log', maxBytes=5242, backupCount=1)
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


def main():

    rep_thread = ReplyThread()
    rep_thread.daemon = True

    rep_thread.run()

    pass


if __name__ == "__main__":
    main()
