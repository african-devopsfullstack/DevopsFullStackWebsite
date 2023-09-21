import mysql.connector as mysql
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

try:
    config = {
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'database': os.getenv('DB_NAME')
    }


    conn = mysql.connect(**config)
    if conn.is_connected():
        print("Connected to MySQL database")
except Error as e:
    print(e)
    pass

def get_connection():
    print("Opened database successfully")
    return conn
    
def create_table():
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT, fname VARCHAR(255) NOT NULL, lname VARCHAR(255) NOT NULL, \
                   gender VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL UNIQUE, password VARCHAR(255) NOT NULL, \
                   phone_number VARCHAR(255), linkedin_profile VARCHAR(255), github_profile VARCHAR(255), about VARCHAR(255), \
                   user_location VARCHAR(255), working_at VARCHAR(255), primary key(id))')
    print("Table created successfully")
    

def insert_table(fname, lname, gender, email, password, phone_number):
    query = f"INSERT INTO users(fname, lname, gender, email, password, phone_number) VALUES(%s, %s, %s, %s, %s, %s)"
    cursor = conn.cursor()
    cursor.execute(query, (fname, lname, gender, email, password, phone_number))
    conn.commit()
    print("Records inserted successfully")
    

def get_user(email):
    query = f"SELECT * FROM devopsFullStack_users WHERE email={email}"
    cursor = conn.cursor()
    result = cursor.execute(query)
    for row in result:
        return row
    

def get_all_users(id: int):
    try:
        query = f"SELECT * FROM devopsFullStack_users WHERE id not in ({id})"
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(e)
        return None

def get_all_posts():
    try:
        query = f"""SELECT
        devopsFullStack_posts.post_id AS post_id,
        devopsFullStack_users.fname as first_name,
        devopsFullStack_users.lname as last_name,
        devopsFullStack_posts.post_content AS post_content,
        (
            SELECT TIMESTAMPDIFF(HOUR, devopsFullStack_posts.created_at, NOW())
            FROM devopsFullStack_posts
            WHERE devopsFullStack_posts.user_id = devopsFullStack_users.id
        ) AS time_elapsed_seconds
    FROM
        devopsFullStack_users
    INNER JOIN
        devopsFullStack_posts ON devopsFullStack_users.id = devopsFullStack_posts.user_id;"""
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
        
    except Exception as e:
        print(e)
        
        return None
    # for row in result:
    #     return row


def comments(user_id, post_id, comment_text, likes, dislikes, parent_comment_id, created_at):
    query = f"INSERT INTO devopsfullstack_user_comments(user_id, post_id, comment_text, likes, dislikes, parent_comment_id, created_at) VALUES(%s, %s, %s, %s, %s, %s, %s)"
    cursor = conn.cursor()
    cursor.execute(query, (user_id, post_id, comment_text, likes, dislikes, parent_comment_id, created_at))
    conn.commit()
    print("Records inserted successfully")
    

# create_table()

# print(get_all_posts())

# print(get_all_users(4))