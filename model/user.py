import sqlite3
import hashlib

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = self.encrypt_password(password)

    def __str__(self):
        return f"User: {self.username}, Password: {self.password}"

    def encrypt_password(self, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

    @staticmethod
    def create_table():
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def save_to_db(self):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (username, password)
                VALUES (?, ?)
            ''', (self.username, self.password))
            conn.commit()
        except sqlite3.IntegrityError:
            print(f"El usuario '{self.username}' ya existe.")
        finally:
            conn.close()

User.create_table()

user = User(username="david", password="password123")

user.save_to_db()

print("Usuario guardado en la base de datos con contraseña encriptada")
