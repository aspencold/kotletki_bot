import sqlite3

DB_NAME = 'recipes.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            time TEXT,
            category TEXT,
            tags TEXT,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_recipe(data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO recipes (title, time, category, tags, description)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['title'], data['time'], data['category'], ','.join(data['tags']), data['description']))
    conn.commit()
    conn.close()

def get_random_recipe(filter_value=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    if filter_value:
        q = f"""
            SELECT title, time, category, tags, description FROM recipes
            WHERE category=? OR tags LIKE ?
            ORDER BY RANDOM() LIMIT 1
        """
        c.execute(q, (filter_value, f'%{filter_value}%'))
    else:
        c.execute("SELECT title, time, category, tags, description FROM recipes ORDER BY RANDOM() LIMIT 1")
    result = c.fetchone()
    conn.close()
    return result