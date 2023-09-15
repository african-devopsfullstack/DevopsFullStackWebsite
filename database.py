import mysql.connector as mysql
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()


config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME')
}


conn = mysql.connect(**config)

def get_connection():
    print("Opened database successfully")
    return conn
    
def create_table():
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT, fname VARCHAR(255) NOT NULL, lname VARCHAR(255) NOT NULL, gender VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL UNIQUE, password VARCHAR(255) NOT NULL, phone_number VARCHAR(255), primary key(id))')
    print("Table created successfully")
    conn.close()

def insert_table(fname, lname, gender, email, password, phone_number):
    query = f"INSERT INTO users(fname, lname, gender, email, password, phone_number) VALUES(%s, %s, %s, %s, %s, %s)"
    cursor = conn.cursor()
    cursor.execute(query, (fname, lname, gender, email, password, phone_number))
    conn.commit()
    print("Records inserted successfully")
    conn.close()

def get_user(email):
    query = f"SELECT * FROM users WHERE email={email}"
    cursor = conn.cursor()
    result = cursor.execute(query)
    for row in result:
        return row
    conn.close()
