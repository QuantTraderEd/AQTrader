# -*- coding: utf-8 -*-

import logging
import sqlite3
import pandas as pd

from publish_thread import PublishThread


def main():
    pub_thread = PublishThread()
    pub_thread.run()
    pass


if __name__ == "__main__":
    main()
