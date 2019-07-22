# -*- coding: utf-8 -*-


import redis
from commutil.FeedCodeList import FeedCodeList


class OptionPrice(object):
    def __init__(self):
        super(OptionPrice, self).__init__()
        self.redis_client = redis.Redis()
        self.ask1_dict = dict()
        self.bid1_dict = dict()
        self._FeedCodeList = FeedCodeList()
        self.strike_list = list()
        self.expire_code_list = list()
        self.expire_month_code = ''
        self.atm_strike = ''
        pass

    def init_quote_dict(self):
        self.bid1_dict = self.redis_client.hgetall('bid1_dict')
        self.ask1_dict = self.redis_client.hgetall('ask1_dict')
        for shortcd in self.bid1_dict.keys():
            if self.bid1_dict[shortcd] is not None:
                self.bid1_dict[shortcd] = float(self.bid1_dict[shortcd])
            else:
                self.bid1_dict[shortcd] = 0.0

        for shortcd in self.ask1_dict.keys():
            if self.ask1_dict[shortcd] is not None:
                self.ask1_dict[shortcd] = float(self.ask1_dict[shortcd])
            else:
                self.ask1_dict[shortcd] = 0.0
        pass

    def init_strike_list(self):
        self._FeedCodeList.read_code_list()
        option_shortcd_lst = self._FeedCodeList.option_shortcd_list
        self.expire_code_list = list(set([shortcd[3:5] for shortcd in option_shortcd_lst]))
        self.expire_code_list.sort()
        self.expire_month_code = self.expire_code_list[1]
        self.strike_list = list(set([shortcd[-3:] for shortcd in option_shortcd_lst
                                   if shortcd[3:5] == self.expire_month_code]))
        self.strike_list.sort(reverse=True)
        pass

    def find_atm_strike(self):
        put_call_parity_min = 99999
        atm_strike = ''
        for strike in self.strike_list:
            call_shortcd = '201' + self.expire_code_list[0] + strike
            put_shortcd = '301' + self.expire_code_list[0] + strike

            bid1 = self.bid1_dict.get(call_shortcd, 0.0)
            ask1 = self.ask1_dict.get(call_shortcd, 0.0)
            if int(bid1 * 100) == 0 or int(ask1 * 100) == 0: continue
            call_mid = (ask1 + bid1) * 0.5

            bid1 = self.bid1_dict.get(put_shortcd, 0.0)
            ask1 = self.ask1_dict.get(put_shortcd, 0.0)
            if int(bid1 * 100) == 0 or int(ask1 * 100) == 0: continue
            put_mid = (ask1 + bid1) * 0.5

            put_call_parity = abs(call_mid - put_mid)
            if put_call_parity_min > put_call_parity:
                put_call_parity_min = put_call_parity
                atm_strike = strike

        self.atm_strike = atm_strike
        return atm_strike
        pass

    def find_target_shortcd(self, callput):
        target_shortcd = None
        min_bid1 = 9999
        if callput == 'call':
            self.strike_list.sort(reverse=True)
            shortcd = '201' + self.expire_month_code + self.strike_list[0]
            bid1 = self.bid1_dict.get(shortcd, 0.0)
            ask1 = self.ask1_dict.get(shortcd, 0.0)
            mid = (ask1 + bid1) * 0.5
            if 0.15 < mid < 0.60: return shortcd
            for strike in self.strike_list:
                if int(strike) < int(self.atm_strike) * 1.10: continue
                shortcd = '201' + self.expire_month_code + strike
                bid1 = self.bid1_dict.get(shortcd, 0.0)
                ask1 = self.ask1_dict.get(shortcd, 0.0)
                bid_ask_spread = ask1 - bid1
                if 0 < bid_ask_spread <= 0.03 and 0.03 <= bid1 <= 0.15 and min_bid1 > bid1:
                    min_bid1 = bid1
                    target_shortcd = shortcd

            return target_shortcd
        elif callput == 'put':
            self.strike_list.sort()
            shortcd = '301' + self.expire_month_code + self.strike_list[0]
            bid1 = self.bid1_dict.get(shortcd, 0.0)
            ask1 = self.ask1_dict.get(shortcd, 0.0)
            mid = (ask1 + bid1) * 0.5
            if 0.15 < mid < 0.60: return shortcd

            for strike in self.strike_list:
                if int(strike) > int(self.atm_strike) * 0.90: continue
                shortcd = '301' + self.expire_month_code + strike
                bid1 = self.bid1_dict.get(shortcd, 0.0)
                ask1 = self.ask1_dict.get(shortcd, 0.0)
                bid_ask_spread = ask1 - bid1
                if 0 < bid_ask_spread <= 0.03 and 0.10 <= bid1 <= 0.15 and min_bid1 > bid1:
                    min_bid1 = bid1
                    target_shortcd = shortcd

            return target_shortcd
        else:
            return target_shortcd
        pass
