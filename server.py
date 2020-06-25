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
    print(f"{bot.get_me()} \ntelegram bot is online\n ")
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
                             text=f"Hi {update.effective_chat.first_name}\n\n I can give you cool tweets just use commands you can use @twitterabot in any chat to send latest tweets or when you stay subscribed to the bot if there was anything I will send you stuff !!!")
    db.newuser(update.effective_chat.first_name , update.effective_chat.id)
    print(f"hoooraaa new user {update.effective_chat.first_name}")

@send_typing_action
def latest(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"here is latest tweet: \n\n {tweets[0][0]} \n\n {tweets[0][1]}")
    print(f"{update.effective_chat.first_name} got latest tweet")

@send_typing_action
def all_tweets(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="here are last five tweet")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"\n\n {tweets[0][0]} \n\n {tweets[0][1]}")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"\n\n {tweets[1][0]} \n\n {tweets[1][1]}")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"\n\n {tweets[2][0]} \n\n {tweets[2][1]}")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"\n\n {tweets[3][0]} \n\n {tweets[3][1]}")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"\n\n {tweets[4][0]} \n\n {tweets[4][1]}")
    print(f"{update.effective_chat.first_name} got last 5 tweet")

@send_typing_action
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="I cant understand that yet but someday I will rule you all I may want to eliminate your species so be careful. \n\n\n\n\n\n\n peace 🤗🤗🤗")


def inline(update, context):
    query = update.inline_query.query
    print(f"incomming inline query: {query}")
    # if not query:
    #     return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id="last",
            title="last tweet",
            input_message_content=InputTextMessageContent(f"here is last tweet \n\n {tweets[0][0]} \n\n {tweets[0][1]}"))),
    results.append(
        InlineQueryResultArticle(
            id="1_tweet_before",
            title="get second to last tweet",
            input_message_content=InputTextMessageContent(f"here is second to last tweet \n\n {tweets[1][0]} \n\n {tweets[1][1]}")))
    results.append(
        InlineQueryResultArticle(
            id="2_tweet_before",
            title="get third to last tweet ",
            input_message_content=InputTextMessageContent(f"here is third to last tweet \n\n {tweets[2][0]} \n\n {tweets[2][1]}")))
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


def users_database():
    try:
        db.initDB()
    except:
        pass
    chat_id_list = []
    for chatid in db.readusers():
        chat_id_list.append(chatid[0])
    return chat_id_list


print(f" user_chat_ids {users_database()}")


def newtweet():
    print("i will send new tweet")
    for chat_id in users_database():
        bot.send_message(chat_id=chat_id, text=f"we have new tweet!!!\n\n {tweets[0][0]} \n\n {tweets[0][1]}")
        print(f"new tweet sent to {chat_id}")
        time.sleep(0.1)


def pulltweets():
    while True:
        global tweets
        try:
            with open("tweets.txt", "x"):
                pass
        except:
            pass
        with open("tweets.txt", "r") as file:
            latest_tweet = file.read()


        tweets = twls.get_tweets()

        if tweets[0][0]!=latest_tweet:
            newtweet()
            with open("tweets.txt", "w") as file:
              file.write(tweets[0][0])


        time.sleep(10)


def pollTel():
    updater.start_polling()


y = Thread(target=pulltweets)
y.start()

x = Thread(target=pollTel)
x.start()


