import telegram
import logging
from conf import read_conf
from telegram.ext import Updater, Defaults

"""
bot sdad
"""
defaults = Defaults()
token = read_conf("cfg.ini")
bot = telegram.Bot(token=token, defaults=defaults)
try:
    print(bot.get_me())
except:
    print("error 1")


updater = Updater(bot=bot, use_context=True, defaults=defaults)
