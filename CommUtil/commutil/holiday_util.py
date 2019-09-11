# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

from os import path
import datetime as dt


class HoliDayUtil:
    def __init__(self):
        self.holiday_list = []

    def read_holiday_data(self, filename=''):
        self.holiday_list = []
        if filename == '': filename = path.join(path.dirname(__file__), 'holiday_list.txt')
        with open(filename, 'r') as f:
            while 1:
                line = f.readline()
                if not line: break
                # print(line[:-2])
                date = line[:-2]
                self.holiday_list.append(date)

            f.close()

        return self.holiday_list

    def is_holiday(self, str_date):
        if str_date in self.holiday_list:
            print('today is holiday')
            return True
        else:
            print('today is not holiday')
            return False


if __name__ == "__main__":

    now_dt = dt.datetime.now()
    today = now_dt.strftime('%Y%m%d')

    # today = '20170608'

    holiday_util = HoliDayUtil()
    holiday_util.read_holiday_data('holiday_list.txt')
    is_holiday = holiday_util.is_holiday(today)

    print('is_holiday: %s' % is_holiday)