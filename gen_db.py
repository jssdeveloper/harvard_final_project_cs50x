import sqlite3

conn = sqlite3.connect("songs.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, hash TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS orders (order_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER REFERENCES users(id), status TEXT, total REAL)")
cursor.execute("CREATE TABLE IF NOT EXISTS order_item (item_id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER REFERENCES orders(order_id), record_id INTEGER REFERENCES songs(id), quantity INTEGER, price REAL)")
cursor.connection.commit()