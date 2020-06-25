import sqlite3
import logging


logging.basicConfig(filename="logs", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def initDB():
    chatsDB = sqlite3.connect("chats.db")
    chatsDB_curser = chatsDB.cursor()
    chatsDB_curser.execute("CREATE TABLE users (name text, chat_id integer,PRIMARY KEY (chat_id))")
    chatsDB.commit()
    chatsDB.close()


def newuser(name, chatid):
    chatsDB = sqlite3.connect("chats.db")
    chatsDB_curser = chatsDB.cursor()
    chatsDB_curser.execute("REPLACE INTO users VALUES (?, ?)", (name, chatid))
    chatsDB.commit()
    logging.info(f"subscriber {name} with chat id {chatid} added to DB")
    chatsDB.close()


def readusers ():
    chatsDB = sqlite3.connect("chats.db")
    chatsDB_curser = chatsDB.cursor()
    chatsDB_curser.execute("SELECT chat_id FROM users")
    chat_ids = chatsDB_curser.fetchall()
    chatsDB.close()
    logging.info("reading users")
    return chat_ids


def remove_users():
    chatsDB = sqlite3.connect("chats.db")
    chatsDB_curser = chatsDB.cursor()
    chatsDB_curser.execute("DELETE FROM users")
    chatsDB.commit()
    chatsDB.close()
