import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

username = input("Enter username: ")
password = input("Enter password: ")

cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

conn.commit()
conn.close()

print("User registered!")