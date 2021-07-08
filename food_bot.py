from requests import get
from bs4 import BeautifulSoup
from googlesearch import search
import telegram 
from telegram.ext import Updater, CommandHandler
from telegram import ParseMode
from credentials import bot_token, bot_user_name
from flask import Flask

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

updater = Updater(token=bot_token)
dispatcher = updater.dispatcher
app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def start(update, context):
    intro_text = 'Hi! To use this bot, use /find to check if the food you want \
                  is at the place specified. :) \nThe format is: Food,Place'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=intro_text)

@app.route('/{}'.format(TOKEN), methods=['POST'])
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

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

def main():
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    find_handler = CommandHandler('find', find)
    dispatcher.add_handler(find_handler)

    updater.start_polling()
    updater.idle()

@app.route('/')
def index():
    return '.'

if __name__ == '__main__':
    # note the threaded arg which allow
    # your app to have more than one thread
    app.run(threaded=True)

# if __name__ == '__main__':
#     main()
    