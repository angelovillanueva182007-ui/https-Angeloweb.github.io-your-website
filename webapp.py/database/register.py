import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

username = input("Username: ")
password = input("Password: ")

cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))

result = cursor.fetchone()

if result:
    print("Login successful!")
else:
    print("Invalid username or password")

conn.close()