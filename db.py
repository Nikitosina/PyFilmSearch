import sqlite3


class UsersModel:
    def __init__(self):
        conn = sqlite3.connect('database.db', check_same_thread=False)
        self.conn = conn

    def make_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                 username VARCHAR(50),
                                 password VARCHAR(128),
                                 favorites VARCHAR(255),
                                 status VARCHAR(10)
                                 )''')
        cursor.close()
        self.conn.commit()

    def insert(self, username, password, status):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO users 
                          (username, password, status, favorites) 
                          VALUES (?,?,?,'')''', (username, password, status))
        cursor.close()
        self.conn.commit()

    def fav(self, user_id, film_id):
        cursor = self.conn.cursor()
        cursor.execute('''UPDATE users SET favorites = ?
                          WHERE id = ?''', (str(film_id), user_id))
        cursor.close()
        self.conn.commit()

    def task(self):
        cursor = self.conn.cursor()
        cursor.execute('''ALTER TABLE users
                            ADD favorites TEXT''')
        cursor.close()
        self.conn.commit()

    def replace(self, id, username, password, status):
        cursor = self.conn.cursor()
        cursor.execute('''REPLACE INTO users 
                          (id, username, password, status) 
                          VALUES (?,?,?,?)''', (id, username, password, status))
        cursor.close()
        self.conn.commit()

    def exists(self, username):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (str(username),))
        row = cursor.fetchone()
        return (True, row) if row is not None else (False, None)

    def get(self, id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, username FROM users")
        row = cursor.fetchall()
        return row

    def delete(self, id):
        cursor = self.conn.cursor()
        cursor.execute('''DELETE FROM users WHERE id = ?''', (str(id),))
        cursor.close()
        self.conn.commit()

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()


class FilmsModel:
    def __init__(self):
        conn = sqlite3.connect('database.db', check_same_thread=False)
        self.conn = conn

    def make_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS films
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             name VARCHAR(100),
                             genre VARCHAR(100),
                             director VARCHAR(50),
                             image_url VARCHAR(200),
                             date DATE,
                             time_length TIME,
                             content VARCHAR(9000)
                             )''')
        cursor.close()
        self.conn.commit()

    def insert(self, name, genre, director, image_url, date, time_length='00:00', content=''):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO films
                          (name, genre, director, image_url, date, time_length, content) 
                          VALUES (?,?,?,?,?,?,?)''', (name, genre, director, image_url, date, time_length, content))
        cursor.close()
        self.conn.commit()

    def replace(self, id, img):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM films WHERE id = ?", (str(id)))
        cursor.close()
        self.conn.commit()

    def get(self, film_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM films WHERE id = ?", (str(film_id),))
        row = cursor.fetchone()
        return row

    def get_all(self, id=None, limit=1000, order=False, arg=None):
        cursor = self.conn.cursor()
        if id:
            cursor.execute('''SELECT name, genre, image_url, date, id FROM films WHERE id IN ({})
                              LIMIT {}'''.format(id[:-1], limit))
        elif order and arg:
            cursor.execute(f'''SELECT name, genre, image_url, date, id FROM films 
                              WHERE (name LIKE '%{arg}%' or content LIKE '%{arg}%' or genre LIKE '%{arg}%' or date LIKE '%{arg}%')''')
        elif order:
            cursor.execute('''SELECT name, genre, image_url, date, id FROM films
                              ORDER BY {} DESC
                              LIMIT {}'''.format(order, limit))
        else:
            cursor.execute("SELECT id, name FROM films")
        rows = cursor.fetchall()
        return rows

    def delete(self, news_id):
        cursor = self.conn.cursor()
        cursor.execute('''DELETE FROM films WHERE id = ?''', (str(news_id),))
        cursor.close()
        self.conn.commit()

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()
