import telegram
import twls
import logging
from conf import read_conf
from functools import wraps
from telegram.ext import Updater, Defaults, MessageHandler, Filters, CommandHandler, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton
import time
from threading import Thread
import db

logging.basicConfig(filename="logs", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

defaults = Defaults()
bot = telegram.Bot(token=read_conf("cfg.ini", "token"), defaults=defaults)
try:
    print(bot.get_me())
except:
    pass

updater = Updater(bot=bot, use_context=True, defaults=defaults)
dispatcher = updater.dispatcher

try:
    db.initDB()
except:
    pass


def send_typing_action(func):
    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action="typing")
        return func(update, context, *args, **kwargs)

    return command_func


@send_typing_action
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Hi {update.effective_chat.first_name}\n\n i can give you cool tweets just use commands!!!")
    db.newuser(update.effective_chat.first_name , update.effective_chat.id)

@send_typing_action
def latest(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"here is latest tweet: \n\n\n {tweets[0]}")


@send_typing_action
def all_tweets(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"here are five latest tweet")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{tweets[0]}")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{tweets[1]}")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{tweets[2]}")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{tweets[3]}")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{tweets[4]}")


@send_typing_action
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="I cant understand that yet but someday I will rule you all I may want to eliminate your species so you may watch your mouth. \n\n\n\n\n\n\n peace 🤗🤗🤗")


def inline(update, context):
    query = update.inline_query.query
    print(query)
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id="latest",
            title="latest tweet",
            input_message_content=InputTextMessageContent(f"here is latest tweet \n\n {tweets[0]}"))),
    results.append(
        InlineQueryResultArticle(
            id="1_tweet_before",
            title="get 1 tweet before",
            input_message_content=InputTextMessageContent(f"here is one tweet before \n \n {tweets[1]}")))
    context.bot.answer_inline_query(update.inline_query.id, results)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


start_handler = CommandHandler('start', start)
latest_handler = CommandHandler('latest', latest)
all_handler = CommandHandler("all_tweets", all_tweets)
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
inline_handler = InlineQueryHandler(inline)
unknown_handler = MessageHandler(Filters.command, unknown)

dispatcher.add_handler(echo_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(latest_handler)
dispatcher.add_handler(all_handler)
dispatcher.add_handler(inline_handler)
dispatcher.add_handler(unknown_handler)


def connect_database():
    try:
        db.initDB()
    except:
        logging.error("unable to connect to database")


def newtweet():
    print("i will ssend new tweet")
    #  bot.send_message()
    # print(db.readusers())
    #time.sleep(3)


def pulltweets():
    while True:
        twls.get_tweets()
        global tweets
        try:
            with open("tweets.txt", "x") as file:
                pass
        except:
            pass
        with open("tweets.txt", "r") as file:
            tweetsfile = file.read()

        tweets = twls.get_tweets()

        if tweets==tweetsfile:
            newtweet()

        with open("tweets.txt", "w") as file:
            for item in tweets:
                file.write(item + '\n')

        time.sleep(10)


def pollTel():
    updater.start_polling()


y = Thread(target=pulltweets)
y.start()

x = Thread(target=pollTel)
x.start()

while True:
    time.sleep(6)
    print(tweets[0])
