import requests
from telegram import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.bot import Bot
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.dispatcher import Dispatcher
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.updater import Updater
from telegram.parsemode import ParseMode
from telegram.update import Update
from telegram.ext.callbackqueryhandler import CallbackQueryHandler

bot_token = '5748811715:AAH9EIiQGBpK85wc4sEaZZlbfbHd5ZEOxq0'
updater = Updater(bot_token,
                  use_context=True)

dispatcher: Dispatcher = updater.dispatcher

def start(update: Update, context: CallbackContext):
    keyboard = [[
        InlineKeyboardButton("10037097 - Diego", callback_data='10037097'),
        InlineKeyboardButton("10053624 - Sam", callback_data='10053624')
    ]]
    kbd_layout = [['#10037097', '#10037098'], ['#10037097', '#10037097']]
    kbd = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text="Seleccionar tarjeta", reply_markup=kbd) 


def remove(update: Update, context: CallbackContext):
    """
    method to handle /remove command to remove the keyboard and return back to text reply
    """

    # making a reply markup to remove keyboard
    # documentation: https://python-telegram-bot.readthedocs.io/en/stable/telegram.replykeyboardremove.html
    reply_markup = ReplyKeyboardRemove()

    # sending the reply so as to remove the keyboard
    update.message.reply_text(text="I'm back.", reply_markup=reply_markup)
    pass


def parse_response(response):
    firstElement = response.split("[")[1].split("]")[0].split("{")[1].split("}")[0].split(", ")[10].split("saldo : '")[1].split("'")[0]
    return firstElement


def get_credit(update: Update, context: CallbackContext):
    print(update.message.text)
    bot: Bot = context.bot
    idTarjeta = update.message.text
    response_API = requests.get('http://www.gpssumo.com/movimientos/get_movimientos/' + idTarjeta + '/3')
    data = response_API.text
    saldo = 'Tenes ' + parse_response(data) + ' en la ' + idTarjeta
  
    bot.send_message(
        chat_id=update.effective_chat.id,
        text=saldo,
        parse_mode=ParseMode.HTML,
    )

def button(update, context):
    query: CallbackQuery = update.callback_query
    idTarjeta = query.data
    response_API = requests.get('http://www.gpssumo.com/movimientos/get_movimientos/' + idTarjeta + '/3')
    data = response_API.text
    saldo = 'Tenes ' + parse_response(data) + ' en la ' + idTarjeta
    query.answer()
    query.edit_message_text(text="Tenes " + parse_response(data) + " en la {}".format(idTarjeta))

updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("remove", remove))

# updater.dispatcher.add_handler(MessageHandler(Filters.regex(r"Tarjeta"), get_credit))
updater.dispatcher.add_handler(CommandHandler("consultar", start))
updater.dispatcher.add_handler(CallbackQueryHandler(button))  # handling inline buttons pressing

updater.start_polling()