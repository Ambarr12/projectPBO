import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "",
                database = "psychology_service"
            )
            if self.connection.is_connected():
                print("Koneksi Database Berhasil")
        except Error as e:
            print(f"Gagal Koneksi Database {e}")
    
    def execute_query(self, query, values=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error saat menjalankan queery: {e}")
            return None
    
    def fetch_query(self, query, values=None):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, values)
            return cursor.fetchall()
        except Error as e:
            print(f"Error saat mengambil data: {e}")
            return None