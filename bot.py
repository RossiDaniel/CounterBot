#!/usr/bin/env python
# coding: utf-8

# In[1]:


# This program is dedicated to the public domain under the CC0 license.
#
# THIS EXAMPLE HAS BEEN UPDATED TO WORK WITH THE BETA VERSION 12 OF PYTHON-TELEGRAM-BOT.
# If you're still using version 11.1.0, please see the examples at
# https://github.com/python-telegram-bot/python-telegram-bot/tree/v11.1.0/examples

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from DBHelper import DBHelper
from secret import TELEGRAM_TOKEN

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    start_msg = "Ciao vecchia volpe, questo è un bot per conteggiare i turni di lavoro, premi /help per visionare i vari comandi!."
    dbh = DBHelper()
    dbh.start(str(update.message.chat_id))
    bot.send_message(chat_id=update.message.chat_id, text=start_msg)


def help(bot, update):
    """Send a message when the command /help is issued."""
    help_msg="premi:\n/punch per iniziare o concludere il turno!\n /day per avere le ore lavorate oggi! \n/tot per avere il totale di ore finora lavorate!"
    bot.send_message(chat_id=update.message.chat_id, text=help_msg)

def punch(bot, update):
    """Send a message when the command /help is issued."""
    dbh = DBHelper()
    msg=dbh.shift_press(str(update.message.chat_id))
    bot.send_message(chat_id=update.message.chat_id, text=msg)

def tot(bot, update):
    """Send a message when the command /help is issued."""
    dbh = DBHelper()
    msg=dbh.total_hour(str(update.message.chat_id))
    bot.send_message(chat_id=update.message.chat_id, text=msg)

def day(bot, update):
    """Send a message when the command /help is issued."""
    dbh = DBHelper()
    msg=dbh.day_hour(str(update.message.chat_id))
    bot.send_message(chat_id=update.message.chat_id, text=msg)



def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', bot, update.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TELEGRAM_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("tot", tot))
    dp.add_handler(CommandHandler("punch", punch))
    dp.add_handler(CommandHandler("day", day))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

