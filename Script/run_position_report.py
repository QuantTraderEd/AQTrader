# -*- coding: utf-8 -*-

from __future__ import print_function

import pprint
import datetime as dt
import zmq
import telegram
import redis

from commutil.FeedCodeList import FeedCodeList

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:7001")      # demo
# socket.connect("tcp://127.0.0.1:7000")      # real
socket.setsockopt(zmq.SUBSCRIBE,"")

update_id = None
chat_id = '49417214'

bot = telegram.Bot('253529538:AAEJ3rKLtNRfkCVfphh_4XEPvb1z5G5qbO4')

redis_client = redis.Redis()
feedcode_list = FeedCodeList()
feedcode_list.read_code_list()
futures_shortcd_lst = [feedcode_list.future_shortcd_list[0],
                       feedcode_list.future_shortcd_list[2]]
position_dict = dict()
autotrader_id = 'MiniArb001'


def main():
    now_dt = dt.datetime.now()
    for shortcd in futures_shortcd_lst:
        qty = redis_client.hget(autotrader_id + '_position_dict', shortcd)
        # logger.info('%s positon-> %s' % (shortcd, qty))
        avg_price = redis_client.hget(autotrader_id + '_tradeprice_dict', shortcd)
        # logger.info('%s tradeprice-> %s' % (shortcd, avg_price))
        position_dict[shortcd] = [int(qty or 0), int(avg_price or 0)]


    bot.send_message(chat_id, "start position_report service")
    msg = pprint.pformat(position_dict)
    bot.send_message(chat_id, msg)
    print(now_dt, msg)

    while True:
        msg_dict = socket.recv_pyobj()
        now_dt = dt.datetime.now()
        for shortcd in self.futures_shortcd_lst:
            qty = redis_client.hget(autotrader_id + '_position_dict', shortcd)
            # logger.info('%s positon-> %s' % (shortcd, qty))
            avg_price = redis_client.hget(autotrader_id + '_tradeprice_dict', shortcd)
            # logger.info('%s tradeprice-> %s' % (shortcd, avg_price))
            position_dict[shortcd] = [int(qty or 0), "%.3f" % avg_price]


        msg = pprint.pformat(position_dict)
        bot.send_message(chat_id, msg)
        print(now_dt, msg)


if __name__ == "__main__":
    main()