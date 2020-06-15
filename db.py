import sqlite3




def initDB():
    chatsDB = sqlite3.connect("chats.db")
    chatsDB_curser = chatsDB.cursor()
    chatsDB_curser.execute("CREATE TABLE users (name text, chat_id integer)")
    chatsDB.commit()
    chatsDB.close()

def NewUser(name, chatid):
    chatsDB = sqlite3.connect("chats.db")
    chatsDB_curser = chatsDB.cursor()
    chatsDB_curser.execute("INSERT INTO users VALUES (?, ?)", (name, chatid))
    chatsDB.commit()
    chatsDB.close()
