import sqlite3

class UserPrompt:
    def __init__(self, db_file):
        # create db file if not exist
        open(db_file, 'a').close()
        self.db_file = db_file
        conn = sqlite3.connect(db_file)
        conn.execute('''CREATE TABLE IF NOT EXISTS prompts
                             (user_id TEXT PRIMARY KEY NOT NULL,
                             prompt TEXT NOT NULL);''')
        conn.close()
        self.cache = {}

    def write_prompt(self, user_id, prompt):
        self.cache[user_id] = prompt
        conn = sqlite3.connect(self.db_file)
        conn.execute("INSERT OR REPLACE INTO prompts (user_id, prompt) VALUES (?, ?)", (user_id, prompt))
        conn.commit()
        conn.close()
    
    def delete_prompt(self, user_id):
        if user_id in self.cache:
            del self.cache[user_id]
        conn = sqlite3.connect(self.db_file)
        conn.execute("DELETE FROM prompts WHERE user_id=?", (user_id,))
        conn.commit()
        conn.close()

    def read_prompt(self, user_id):
        if user_id in self.cache:
            return self.cache[user_id]
        else:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.execute("SELECT prompt FROM prompts WHERE user_id=?", (user_id,))
            prompt = cursor.fetchone()
            conn.close()
            if prompt is None:
                return None
            else:
                self.cache[user_id] = prompt[0]
                return prompt[0]

user_prompt = UserPrompt('data/user_prompt.db')


if __name__ == '__main__':
    user_prompt.write_prompt('123', 'test')
    print(user_prompt.read_prompt('123'))