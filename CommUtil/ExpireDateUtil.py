# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import datetime as dt

year_code_list = [
                  u'E',  # 10
                  u'F',  # 11
                  u'G',  # 12
                  u'H',  # 13
                  u'J',  # 14
                  u'K',  # 15
                  u'L',  # 16
                  u'M',  # 17
                  u'N',  # 18
                  u'P',  # 19
                  u'Q',  # 20
                  u'R',  # 21
                  u'S',  # 22
                  u'T',  # 23
                  u'V',  # 24
                  u'W',  # 25
                  u'6',  # 26
                  u'7',  # 27
                  u'8',  # 28
                  u'9',  # 29
                  u'0',  # 30
                  u'1',  # 31
                  u'2',  # 32
                  u'3',  # 33
                  u'4',  # 34
                  u'5',  # 35
                  u'A',  # 36
                  u'B',  # 37
                  u'C',  # 38
                  u'D',  # 39
                  ]

month_code_dict = dict()
month_code_dict['01'] = u'1'
month_code_dict['02'] = u'2'
month_code_dict['03'] = u'3'
month_code_dict['04'] = u'4'
month_code_dict['05'] = u'5'
month_code_dict['06'] = u'6'
month_code_dict['07'] = u'7'
month_code_dict['08'] = u'8'
month_code_dict['09'] = u'9'
month_code_dict['10'] = u'A'
month_code_dict['11'] = u'B'
month_code_dict['12'] = u'C'


class ExpireDateUtil:
    def __init__(self):
        self.expire_date_lst = []
        self.expire_month_lst = []
        self.front_expire_date = ''
        self.back_expire_date = ''

    def read_expire_date(self, filepath='.'):
        self.expire_date_lst = []
        with open(filepath + '/expire_date.txt', 'r') as f:
            while 1:
                line = f.readline()
                if not line: break
                # print(line[:-2])
                date = line[:-2]
                self.expire_date_lst.append(date)
                self.expire_month_lst.append(date[:6])

            # print(self.expire_date_lst)
            f.close()

    def is_expire_date(self, str_date):
        if str_date in self.expire_date_lst:
            print('today is expire date')
            return True
        else:
            return False

    def make_expire_date(self, str_date):
        month_index = self.expire_month_lst.index(str_date[:6])
        expire_date = self.expire_date_lst[month_index]
        if str_date > expire_date:
            self.front_expire_date = self.expire_date_lst[month_index + 1]
            self.back_expire_date = self.expire_date_lst[month_index + 2]
        elif str_date <= expire_date:
            self.front_expire_date = self.expire_date_lst[month_index]
            self.back_expire_date = self.expire_date_lst[month_index + 1]
        return self.front_expire_date, self.back_expire_date

    def make_expire_shortcd(self, str_date):
        self.make_expire_date(str_date)

        year1 = year_code_list[int(self.front_expire_date[:4]) % 30]
        month1 = month_code_dict.get(self.front_expire_date[4:6], '')

        year2 = year_code_list[int(self.back_expire_date[:4]) % 30]
        month2 = month_code_dict.get(self.back_expire_date[4:6], '')

        # print(year1 + month1)
        # print(year2 + month2)
        return year1 + month1, year2 + month2


if __name__ == "__main__":

    now_dt = dt.datetime.now()
    today = now_dt.strftime('%Y%m%d')

    # today = '20170608'

    expiredate_util = ExpireDateUtil()
    expiredate_util.read_expire_date('.')
    is_expiredate = expiredate_util.is_expire_date(today)

    result1 = expiredate_util.make_expire_date(today)
    result2 = expiredate_util.make_expire_shortcd(today)
    print('is_expiredate: %s' % is_expiredate)
    print(result1)
    print(result2)

