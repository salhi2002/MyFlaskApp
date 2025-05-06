# init_db.py
from app import get_connection
import time

time.sleep(5)

conn = get_connection()
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS data (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL
)
""")

cur.execute("INSERT INTO users (username, password) VALUES (%s, %s) ON CONFLICT DO NOTHING", ("admin", "password"))

conn.commit()
conn.close()
