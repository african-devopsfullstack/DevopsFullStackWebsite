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
# try:
#     config = {
#         'user': os.getenv('DB_USER'),
#         'password': os.getenv('DB_PASSWORD'),
#         'host': os.getenv('DB_HOST'),
#         'database': os.getenv('DB_NAME')
#     }


#     
#     if conn.is_connected():
#         print("Connected to MySQL database")
# except Error as e:
#     print(e)
#     pass

# def get_connection():
#     print("Opened database successfully")
#     return conn
    
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT, fname VARCHAR(255) NOT NULL, lname VARCHAR(255) NOT NULL, \
                   gender VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL UNIQUE, password VARCHAR(255) NOT NULL, \
                   phone_number VARCHAR(255), linkedin_profile VARCHAR(255), github_profile VARCHAR(255), about VARCHAR(255), \
                   user_location VARCHAR(255), working_at VARCHAR(255), primary key(id))')
    print("Table created successfully")
    conn.close()

def insert_table(conn, fname, lname, gender, email, password, phone_number):
    query = f"INSERT INTO users(fname, lname, gender, email, password, phone_number) VALUES(%s, %s, %s, %s, %s, %s)"
    cursor = conn.cursor()
    cursor.execute(query, (fname, lname, gender, email, password, phone_number))
    conn.commit()
    print("Records inserted successfully")
    conn.close()

def get_user(conn, email):
    query = f"SELECT * FROM users WHERE email={email}"
    cursor = conn.cursor()
    result = cursor.execute(query)
    for row in result:
        return row
    conn.close()

def get_all_users(conn, id: int):
    try:
        query = f"SELECT * FROM users WHERE id not in ({id})"
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(e)
        return None

def get_all_posts(conn):
    try:
        query = """SELECT
        users.fname as first_name,
        users.lname as last_name,
        posts.post_content AS post_content,
        (
            SELECT MAX(TIMESTAMPDIFF(HOUR, posts.created_at, NOW()))
            FROM posts
            WHERE posts.user_id = users.id
        ) AS time_elapsed_seconds
    FROM
        users
    INNER JOIN
        posts ON users.id = posts.user_id;"""
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
        
    except Exception as e:
        print(e)
        conn.close()
        return None
    # for row in result:
    #     return row

# create_table()

# print(get_all_posts(conn=conn))

# print(get_all_users(0))