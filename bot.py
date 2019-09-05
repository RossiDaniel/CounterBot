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
from telegram import InlineKeyboardButton, InlineKeyboardMarkup,KeyboardButton,ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler,CallbackQueryHandler
from secret import TELEGRAM_TOKEN
import function

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""

    kb = [[KeyboardButton('/start'),KeyboardButton('/help')],[KeyboardButton('/punch'),KeyboardButton('/day')],[KeyboardButton('/tot'),KeyboardButton('/opt')],[KeyboardButton('/add'),KeyboardButton('/reset')]]
    kb_markup = ReplyKeyboardMarkup(kb)

    start_msg = "Ciao vecchia volpe, questo è un bot per conteggiare i turni di lavoro, premi /help per visionare i vari comandi!."
    function.fstart(str(update.message.chat_id))
    bot.send_message(chat_id=update.message.chat_id, text=start_msg,reply_markup=kb_markup)

def help(bot, update):
    """Send a message when the command /help is issued."""
    help_msg="premi:\n/punch per iniziare o concludere il turno!\n/day per avere le ore lavorate oggi! \n/tot per avere il totale di ore lavorate finora!\n/opt per compattare i turni collegati!\n/add per aggiungere delle ore non extra!\n/reset per eliminare tutti i dati!"
    bot.send_message(chat_id=update.message.chat_id, text=help_msg)

def punch(bot, update):
    """Send a message when the command /help is issued."""
    msg=function.fpunch(str(update.message.chat_id))
    bot.send_message(chat_id=update.message.chat_id, text=msg)

def tot(bot, update):
    """Send a message when the command /help is issued."""
    msg=function.ftot(str(update.message.chat_id))
    bot.send_message(chat_id=update.message.chat_id, text=msg)

def day(bot, update):
    """Send a message when the command /help is issued."""
    msg=function.fday(str(update.message.chat_id))
    bot.send_message(chat_id=update.message.chat_id, text=msg)

def opt(bot, update):
    """Send a message when the command /help is issued."""
    msg=function.fopt(str(update.message.chat_id))
    bot.send_message(chat_id=update.message.chat_id, text=msg)

def add(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Aggiungi manualmente ore, per farlo digita il numero di ore e di minuti\nPer esempio: 59:30')
    return 'ADDHOURS'

def reset(bot,update):
    keyboard = [[InlineKeyboardButton("Sì", callback_data='1'),InlineKeyboardButton("No", callback_data='0')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Sicuro di voler resettare?\nTutti i dati andranno perduti:', reply_markup=reply_markup)

def button(bot, update):
    query = update.callback_query
    if int(str(format(query.data))) == 1:
        function.freset(update['callback_query']['message']['chat']['id'])
        query.edit_message_text(text='Dati eliminati con successo!')

    else:
        query.edit_message_text(text='Nessun dato eliminato!')


def addhpurs(bot, update):
    data = update.message.text
    data = data.split(':')
    if len(data) == 2:
        hours = 0
        minute = 0
        try:
            hours = int(data[0])
            minute = int(data[1])
        except ValueError:
            update.message.reply_text("La stringa inserita:\n->\t" + str(update.message.text)+"\t<-\nNon è formata da numeri.")
            return ConversationHandler.END

        if hours > 0 and minute > 0:
            function.fadd(update.message.chat_id,hours*60+minute)
            tot(bot,update)
            return ConversationHandler.END
        else:
            update.message.reply_text("La stringa inserita:\n->\t" + str(update.message.text)+"\t<-\nNon è formata da numeri positivi.")
            return ConversationHandler.END

    
    update.message.reply_text("La stringa inserita:\n->\t" + str(update.message.text)+"\t<-\nNon è nel formato HH:MM.")
    return ConversationHandler.END

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
    dp.add_handler(CommandHandler("opt", opt))
    dp.add_handler(CommandHandler("reset", reset))

    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add)],
        states={'ADDHOURS': [MessageHandler(Filters.text,addhpurs),],},
        fallbacks=[CommandHandler('help', help)]
    )

    dp.add_handler(conv_handler)

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

