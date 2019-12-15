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

import datetime as dt
import logging
import pprint
import redis
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from commutil.FeedCodeList import FeedCodeList

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

redis_client = redis.Redis()
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
    now_dt = dt.datetime.now()
    for shortcd in futures_shortcd_lst:
        qty = redis_client.hget(autotrader_id + '_liveqty_dict', shortcd)
        liveqty_dict[shortcd] = int(qty or 0)

    msg = pprint.pformat(liveqty_dict)
    bot.send_message(update.message.chat_id, msg)
    print(now_dt, msg)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("253529538:AAEJ3rKLtNRfkCVfphh_4XEPvb1z5G5qbO4")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("liveqty", report_liveqty))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler([Filters.text], echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

