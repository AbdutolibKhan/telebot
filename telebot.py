
from telegram import InlineKeyboardButton,InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler,Filters

BTN_TODAY, BTN_TOMORROW, BTN_MONTH, BTN_REGION, BTN_DUA = ('bugun', 'ertaga','toliq taqvim','🇺🇿mintaqa','Duo')
main_buttons = ReplyKeyboardMarkup([
    [BTN_TODAY], [BTN_TOMORROW],[BTN_MONTH],[BTN_REGION],[BTN_DUA]
], resize_keyboard=True)

STATE_REGION = 1
STATE_CALENDAR = 2

def start(update, context):
    user = update.message.from_user

    buttons = [
        [
            InlineKeyboardButton('Toshkent', callback_data='region_1'),
            InlineKeyboardButton('Andijon', callback_data='region_2')
        ]
    ]
    update.message.reply_html('Salom'. format(user.first_name), reply_markup=InlineKeyboardMarkup(buttons) )

    return STATE_REGION

def inline_callback(update, context):
   query = update.callback_query
   query.message.delete()
   query.message.reply_html(text='<b> 🗾 Ramazon taqvimi</b>\n \n quyydagilardan birini tanlang',parse_mode="HTML", reply_markup=main_buttons)

   return STATE_CALENDAR

def calendar_today(update, context):
    update.message.reply_text('bugun belgilandi')


def calendar_tomorrow(update, context):
    update.message.reply_text('ertaga belgilandi')

def calendar_month(update, context):
    update.message.reply_text('toliq taqvim belgilandi')

def calendar_region(update, context):
    update.message.reply_text('mintaqa belgilandi')

def calendar_dua(update, context):
    update.message.reply_text('duo belgilandi')


def main ():
    updater = Updater('1437771700:AAFb0L544VRzUALEow4dDwAv_TvuVPZCOeE', use_context=True)

    dispatcher = updater.dispatcher

    #dispatcher.add_handler(CommandHandler('start', start))

    #dispatcher.add_handler(CallbackQueryHandler(inline_callback))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start',start)],
        states={
            STATE_REGION:[CallbackQueryHandler(inline_callback)],
            STATE_CALENDAR:[MessageHandler(Filters.regex('^('+BTN_TODAY+')$'),calendar_today),
                            MessageHandler(Filters.regex('^('+BTN_TOMORROW+')$'),calendar_tomorrow),
                            MessageHandler(Filters.regex('^(' + BTN_MONTH + ')$'), calendar_month),
                            MessageHandler(Filters.regex('^(' + BTN_REGION + ')$'), calendar_region),
                            MessageHandler(Filters.regex('^(' + BTN_DUA + ')$'), calendar_dua),
                            ],
        },
        fallbacks=[CommandHandler('start', start)]
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


main()



