import sqlite3

conn = sqlite3.connect("database.db")
print("database opened successfully")

conn.execute("CREATE TABLE assignments (id INTEGER PRIMARY KEY, name TEXT, mentor TEXT, leader TEXT, deadline DATE)")
print("table created successfully")

conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL)")
print("table created successfully")


conn.close()