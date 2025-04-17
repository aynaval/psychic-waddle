import sqlite3

conn = sqlite3.connect("orders.db")
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS orders')  # Drop old table

cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    product TEXT NOT NULL,
    quantity TEXT NOT NULL,  -- <-- Now TEXT
    email TEXT NOT NULL
)
''')

conn.commit()
conn.close()
