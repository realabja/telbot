import sqlite3
import logging


logging.basicConfig(filename="logs", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def initDB():
    chatsDB = sqlite3.connect("chats.db")
    chatsDB_curser = chatsDB.cursor()
    chatsDB_curser.execute("CREATE TABLE users (name text, chat_id integer)")
    chatsDB.commit()
    chatsDB.close()


def newuser(name, chatid):
    chatsDB = sqlite3.connect("chats.db")
    chatsDB_curser = chatsDB.cursor()
    chatsDB_curser.execute("INSERT INTO users VALUES (?, ?)", (name, chatid))
    chatsDB.commit()
    logging.info(f"subscriber {name} with chat id {chatid} added to DB")
    chatsDB.close()


def readusers ():
    chatsDB = sqlite3.connect("chats.db")
    chatsDB_curser = chatsDB.cursor()
    chatsDB_curser.execute("SELECT chat_id from users")
    chat_ids = chatsDB_curser.fetchall()
    chatsDB.close()
    return chat_ids

