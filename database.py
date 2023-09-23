import mysql.connector as mysql
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()
# config = {
#         'user': os.getenv('DB_USER'),
#         'password': os.getenv('DB_PASSWORD'),
#         'host': os.getenv('DB_HOST'),
#         'database': os.getenv('DB_NAME')
#     }


# conn = mysql.connect(**config)


def get_connection(conn):
    print("Opened database successfully")
    return conn
    
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT, fname VARCHAR(255) NOT NULL, lname VARCHAR(255) NOT NULL, \
                   gender VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL UNIQUE, password VARCHAR(255) NOT NULL, \
                   phone_number VARCHAR(255), linkedin_profile VARCHAR(255), github_profile VARCHAR(255), about VARCHAR(255), \
                   user_location VARCHAR(255), working_at VARCHAR(255), primary key(id))')
    print("Table created successfully")
    

def insert_table(conn, fname, lname, gender, email, password, phone_number):
    query = "INSERT INTO users(fname, lname, gender, email, password, phone_number) VALUES(%s, %s, %s, %s, %s, %s)"
    cursor = conn.cursor()
    cursor.execute(query, (fname, lname, gender, email, password, phone_number))
    conn.commit()
    print("Records inserted successfully")
    

def get_user(conn, email):
    query = f"SELECT * FROM users WHERE email={email}"
    cursor = conn.cursor()
    result = cursor.execute(query)
    for row in result:
        return row
    

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
        posts.post_id AS post_id,
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
        
        return None
    # for row in result:
    #     return row


def comments(conn, user_id, post_id, comment_text, likes, dislikes, parent_comment_id, created_at):
    query = "INSERT INTO user_comments(user_id, post_id, comment_text, likes, dislikes, parent_comment_id, created_at) VALUES(%s, %s, %s, %s, %s, %s, %s)"
    cursor = conn.cursor()
    cursor.execute(query, (user_id, post_id, comment_text, likes, dislikes, parent_comment_id, created_at))
    conn.commit()
    print("Records inserted successfully")
    

# create_table()

# print(get_all_posts())

# print(get_all_users(4))