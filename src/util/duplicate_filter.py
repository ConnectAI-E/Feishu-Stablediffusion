
# Store the processed records in sqlite
from datetime import datetime
import os
import sqlite3
from util.logger import app_logger

DB_PATH = "data/processed_records.db"
inited = False
processed_map = {}


def init():
    global inited
    global processed_map
    if inited:
        return

    if not os.path.exists(DB_PATH):
        db_dir = os.path.dirname(DB_PATH)
        os.mkdir(db_dir)
        # create an empty database file
        open(DB_PATH, 'a').close()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # table schema: id, timestamp
        c.execute(
            "CREATE TABLE IF NOT EXISTS records (id TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
        conn.commit()
        conn.close()
    else:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # fetch records within one day
        c.execute(
            "SELECT * FROM records WHERE timestamp > datetime('now', '-1 day')")
        rows = c.fetchall()
        for row in rows:
            processed_map[row[0]] = row[1]
        app_logger.debug("init processed records: %s", processed_map)
        c.execute("DELETE FROM records WHERE timestamp < datetime('now', '-1 day')")
        conn.commit()
        conn.close()
    inited = True


def is_processed(message_id):
    init()
    global processed_map
    app_logger.debug("processed_map: %s", processed_map)
    app_logger.debug("message_id: %s", message_id)
    if message_id in processed_map:
        return True

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM records WHERE id = ?", (message_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return True

    return False


def event_is_processed(event):
    return is_processed(event.event.message.message_id)


def bot_event_is_processed(event):
    return is_processed(event["token"])

def mark_processed(id):
    processed_map[id] = True
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # insert value with id and current timestamp
    now = datetime.now()
    c.execute("INSERT INTO records VALUES (?, ?)", (id, now))
    conn.commit()
    conn.close()

def unmark_processed(id):
    processed_map.pop(id)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # delete value with id
    c.execute("DELETE FROM records WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def mark_bot_event_processed(event):
    mark_processed(event["token"])


def mark_event_processed(event):
    mark_processed(event.event.message.message_id)

def unmark_event_processed(event):
    unmark_processed(event.event.message.message_id)
