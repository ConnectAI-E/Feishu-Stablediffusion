import os
import sqlite3
from attr import dataclass
from util.logger import app_logger

CHAT_HISTORY_DB_FILE = 'data/chat_history.db'

@dataclass(init=False)
class ChatEvent:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    user_id: str
    chat_id: str
    chat_type: str
    message_id: str
    message_type: str
    content: str
    create_time: int
    sender_user_id: str

def init_db_if_required():
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists('data/chat_history.db'):
        open(CHAT_HISTORY_DB_FILE, 'w').close()
    conn = sqlite3.connect(CHAT_HISTORY_DB_FILE)
    c = conn.cursor()
    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS chat_event
                 (user_id text, chat_id text, chat_type text, message_id text, message_type text, content text, create_time integer,sender_user_id text)''')
    conn.commit()
    conn.close()

def get_chat_context_by_user_id(user_id: str):
    conn = sqlite3.connect(CHAT_HISTORY_DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM chat_event WHERE user_id = ? order by create_time desc limit 20", (user_id,))
    rows = c.fetchall()
    result = [ChatEvent(**dict(zip([column[0] for column in c.description], row))) for row in rows[::-1]]
    conn.close()
    return result

def clean_chat(user_id:str):
    conn = sqlite3.connect(CHAT_HISTORY_DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM chat_event WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def append_chat_event(chat_event: ChatEvent):
    conn = sqlite3.connect(CHAT_HISTORY_DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO chat_event VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (chat_event.user_id, chat_event.chat_id, chat_event.chat_type, chat_event.message_id, chat_event.message_type, chat_event.content, chat_event.create_time, chat_event.sender_user_id))
    conn.commit()
    conn.close()


def get_all_chat_events():
    conn = sqlite3.connect(CHAT_HISTORY_DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM chat_event")
    rows = c.fetchall()
    conn.close()
    for row in rows:
        app_logger.info(row)

if __name__ == '__main__':
    get_all_chat_events()
    # app_logger.info(get_chat_context_by_user_id("ab1cd2ef"))

