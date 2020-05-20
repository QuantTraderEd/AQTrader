# -*- coding: utf-8 -*-

import logging
import sqlite3
import pandas as pd

from logging.handlers import RotatingFileHandler

from publish_thread import PublishThread

logger = logging.getLogger('DataReplayer')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('DataReplayer.log')
fh = RotatingFileHandler('DataReplayer.log', maxBytes=5242, backupCount=3)
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
    pub_thread = PublishThread()
    pub_thread.run()
    pass


if __name__ == "__main__":
    main()
