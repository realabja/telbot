import telegram
import twls
import logging
from conf import read_conf
from functools import wraps
from telegram.ext import Updater, Defaults, MessageHandler, Filters, CommandHandler, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton
import time
from threading import Thread



logging.basicConfig(filename="logs", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)





defaults = Defaults()
bot = telegram.Bot(token=read_conf("cfg.ini","token"), defaults=defaults)
try:
    print(bot.get_me())
except:
    pass


updater = Updater(bot=bot, use_context=True, defaults=defaults)
dispatcher = updater.dispatcher

def send_typing_action(func):


    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action="typing")
        return func(update, context,  *args, **kwargs)

    return command_func

@send_typing_action
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")



@send_typing_action
def latest(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"here is latest tweet \n {tweet}")

@send_typing_action
def all_tweets(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"here are five latest tweet")

    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{tweet}")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{tweeturl1}")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{tweeturl2}")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{tweeturl3}")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{tweeturl4}")



@send_typing_action
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

    print(update.message.chat_id)
    print(update.message.text)

def inline_caps(update, context):
    query = update.inline_query.query
    print(query)
    if not query:
        return
    results = list()


    results.append(
        InlineQueryResultArticle(
            id="latest",
            title="latest tweet",
            input_message_content=InputTextMessageContent(f"here is latest tweet \n {tweet}"))),
    results.append(
        InlineQueryResultArticle(
            id="all_tweets",
            title="get all tweets",
            input_message_content=InputTextMessageContent("i cant give more then one tweet at once")
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")




tweeturl1 = "https://twitter.com/nixcraft/status/1257523899060719623?s=20"
tweeturl2 = "https://twitter.com/huazy12/status/1268533122880212993?s=20"
tweeturl3 = "https://twitter.com/nixcraft/status/1272237201661677568?s=20"
tweeturl4 = "https://twitter.com/nixcraft/status/1271893020443463681?s=20"
start_handler = CommandHandler('start', start)
latest_handler = CommandHandler('latest', latest)
all_handler = CommandHandler("all_tweets", all_tweets)
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
inline_caps_handler = InlineQueryHandler(inline_caps)
unknown_handler = MessageHandler(Filters.command, unknown)


dispatcher.add_handler(echo_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(latest_handler)
dispatcher.add_handler(all_handler)
dispatcher.add_handler(inline_caps_handler)
dispatcher.add_handler(unknown_handler)

tweets = []
tweet = ""
def pullTweets():
    while True :
        twls.get_tweets()
        global tweets
        global tweet
        tweets = twls.get_tweets()
        tweet = tweets[0][1] + " " + tweets[0][0]
        time.sleep(10)
def pollTel():
    updater.start_polling()


y = Thread(target=pullTweets)
y.start()

x = Thread(target=pollTel)
x.start()

while True:
    time.sleep(1)
    print(tweet)
