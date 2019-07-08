# -*- coding: utf-8 -*-

# from ..pycybos import CpCybos
from CommUtil.commutil.ExpireDateUtil import ExpireDateUtil


class TestClass(object):
    expire_date_util = ExpireDateUtil()
    expire_date_util.read_expire_date()

    def test_make_expire_shortcd(self):
        target_date_list = [
                            '20171103',
                            '20180103',
                            '20190103',
                            '20200103',
#                             '20210103',
#                             '20220103',
#                             '20230103',
#                             '20240103',
#                             '20250103',
#                             '20260103',
#                             '20270104',
                            ]

        expire_code_check_dict = dict()
        expire_code_check_dict['20171103'] = ('MB', 'MC')
        expire_code_check_dict['20180103'] = ('N1', 'N2')
        expire_code_check_dict['20190103'] = ('P1', 'P2')
        expire_code_check_dict['20200103'] = ('Q1', 'Q2')

        for target_date in target_date_list:
            expire_month_code_list = self.expire_date_util.make_expire_shortcd(target_date)
            assert expire_month_code_list == expire_code_check_dict[target_date]

