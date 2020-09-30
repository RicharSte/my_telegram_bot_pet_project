import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from handlers import (get_planet, greet_user, next_full_moon, word_count,
                      calc, cities11, user_coordinates, talk_to_me, check_user_photo)
from settings import BOT_TOKEN, PROXY

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
)


PROXY = {
    'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {
        'username': 'learn', 
        'password': 'python'
    }
}


def main():
    mybot = Updater(BOT_TOKEN, use_context = True) #request_kwargs=PROXY)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler("planet", get_planet))
    dp.add_handler(CommandHandler("wordcount", word_count))
    dp.add_handler(CommandHandler("calc", calc))
    dp.add_handler(CommandHandler("next_full_moon", next_full_moon))
    dp.add_handler(CommandHandler('city', cities11))
    dp.add_handler(MessageHandler(Filters.photo, check_user_photo))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    
    mybot.start_polling()
    mybot.idle()
       

if __name__ == "__main__":
    main()
