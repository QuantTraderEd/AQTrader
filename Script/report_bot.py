# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from __future__ import print_function

import logging
import pprint
import datetime
import redis
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from commutil.FeedCodeList import FeedCodeList

# Enable logging
logger = logging.getLogger('report_bot')
logger.setLevel(logging.INFO)

# create file handler which logs even debug messages
fh = logging.FileHandler('report_bot.log')
# fh = logging.Handlers.RotatingFileHandler('ZeroOMS.log',maxBytes=104857,backupCount=3)
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s.%(msecs)03d [%(levelname)s] '                              
                              '%(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handler to logger
logger.addHandler(fh)
logger.addHandler(ch)


redis_client = redis.Redis(port=6479)
feedcode_list = FeedCodeList()
feedcode_list.read_code_list()
futures_shortcd_lst = [feedcode_list.future_shortcd_list[0],
                       feedcode_list.future_shortcd_list[2]]
liveqty_dict = dict()
autotrader_id = 'MiniArb001'


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)


def report_liveqty(bot, update):
    for shortcd in futures_shortcd_lst:
        qty = redis_client.hget(autotrader_id + '_liveqty_dict', shortcd)
        liveqty_dict[shortcd] = int(qty or 0)

    msg = pprint.pformat(liveqty_dict)
    msg = 'liveqty: ' + msg
    bot.send_message(update.message.chat_id, msg)
    logger.info(msg)


def report_pnl(bot, update):
    pnl_dict = redis_client.hgetall('pnl_dict')
    msg = pprint.pformat(pnl_dict)
    bot.send_message(update.message.chat_id, msg)
    logger.info(msg)


def report_position(bot, update):
    position_dict = redis_client.hgetall(autotrader_id + '_position_dict')
    msg = pprint.pformat(position_dict)
    bot.send_message(update.message.chat_id, msg)
    logger.info(msg)


def report_live_orderbook_dict(bot, update):
    str_dict = redis_client.get(autotrader_id + '_live_orderbook_dict')
    if str_dict is not None:
        live_orderbook_dict = eval(str_dict)
    else:
        live_orderbook_dict = dict()
    msg = pprint.pformat(live_orderbook_dict)
    bot.send_message(update.message.chat_id, msg)
    logger.info(msg)


def error(bot, update, error_msg):
    logger.warn('Update "%s" caused error "%s"' % (update, error_msg))


def main():
    chat_id = '49417214'
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("253529538:AAEJ3rKLtNRfkCVfphh_4XEPvb1z5G5qbO4")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("liveqty", report_liveqty))
    dp.add_handler(CommandHandler("pnl", report_pnl))
    dp.add_handler(CommandHandler("position", report_position))
    dp.add_handler(CommandHandler("live_orderbook", report_live_orderbook_dict))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler([Filters.text], echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    logger.info('start report_bot service')
    updater.bot.send_message(chat_id, 'start report_bot service')

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

