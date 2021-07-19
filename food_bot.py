import logging
from requests import get
from bs4 import BeautifulSoup
from googlesearch import search
import telegram 
from telegram.ext import Updater, CommandHandler
from telegram import ParseMode
from credentials import bot_token, bot_user_name, URL
from functions import clean_text
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', 8443))
global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

updater = Updater(token=bot_token)
dispatcher = updater.dispatcher

replace = [' ', '-', "'"]
replacement = [''] * len(replace)

def start(update, context):
    intro_text = 'Hi! To use this bot, use /find to check if the food you want \
                  is at the place specified. :) \nThe format is: /find Food,Place'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=intro_text)

def find(update, context):
    query = update.message.text
    flag = 1
    query = query.replace('/find', '')

    if ',' in query:
        try:
            food = query.split(',')[0]
            place = query.split(',')[1]
        except:
            wrong_format = 'Too many , in the query, please follow the format'
            context.bot.send_message(chat_id=update.message.chat_id, 
                                     text=wrong_format)

        response = search(f'Singapore {food} {place}')
        re_food = clean_text(food, replace, replacement)
        re_place = clean_text(place, replace, replacement)

        for res in response:
            url = res
            res = clean_text(res, replace, replacement, url=True)
            if re_food in res and re_place in res:
                text_result = f'{food} can be found at{place}.\nMore Information at {url}'
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text=text_result)
                flag = 0
                break
        if flag == 1:
            text_result = f'{place} does not have {food}'
            context.bot.send_message(chat_id=update.message.chat_id,
                                        text=text_result)
    else:
        wrong_input = 'Unable to detect input, did you forget the ,'
        context.bot.send_message(chat_id=update.message.chat_id, 
                                 text=wrong_input)

def main():
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    find_handler = CommandHandler('find', find)
    dispatcher.add_handler(find_handler)

    # updater.start_polling()

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url=URL + TOKEN)

    updater.idle()

if __name__ == '__main__':
    main()
    