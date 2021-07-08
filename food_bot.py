import logging
from requests import get
from bs4 import BeautifulSoup
from googlesearch import search
import telegram 
from telegram.ext import Updater, CommandHandler
from telegram import ParseMode
from credentials import bot_token, bot_user_name, URL
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

def start(update, context):
    intro_text = 'Hi! To use this bot, use /find to check if the food you want \
                  is at the place specified. :) \nThe format is: Food,Place'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=intro_text)

def find(update, context):
    query = update.message.text
    flag = 1
    query = query.replace('/find', '')

    if ',' in query:
        try:
            food = query.split(',')[0]
            food = food.replace(' ', '').lower()
            
            place = query.split(',')[1]
            place = place.replace(' ', '').lower()
        except:
            error_format = 'Too many , in the query, please follow the format'
            context.bot.send_message(chat_id=update.message.chat_id, 
                                     text=error_format)

        response = search(f'Singapore {food} {place}')[:2]

        for res in response:
            if food in res and place in res:
                text_result = f'{food} can be found at {place}. \
                                More Information can be found at {res}'
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text=text_result)
                flag = 0
                break
        
        if flag == 1:
            text_result = f'{place} does not have {food}'
            context.bot.send_message(chat_id=update.message.chat_id,
                                        text=text_result)

def main():
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    find_handler = CommandHandler('find', find)
    dispatcher.add_handler(find_handler)

    # updater.start_polling()

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)

    updater.bot.setWebhook(URL + TOKEN)

    updater.idle()

if __name__ == '__main__':
    main()
    