# db_connect.py

import mysql.connector
from mysql.connector import Error
from Config import DB_CONFIG

def create_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("Connected to the database.")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None
