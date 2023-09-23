from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
import sqlite3
from flaskext.mysql import MySQL
from mysql.connector import connect, Error
from flask_cors import CORS
from functools import wraps
from flask_wtf import FlaskForm
from wtforms import SelectField
from passlib.hash import sha256_crypt
import secrets
import database
from dotenv import load_dotenv
import os
import datetime

load_dotenv()


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
mysql = MySQL()

app.config['FLASK_ENV'] = 'development'
app.config['DEBUG'] = True
app.config['FLASK_APP'] = 'app.py'

# app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST')
# app.config['MYSQL_DATABASE_PORT'] = 3306
# app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER')
# app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('DB_PASSWORD')
# app.config['MYSQL_DATABASE_DB'] = os.getenv('DB_NAME')
# app.config['MYSQL_DATABASE_CHARSET'] = 'utf8'


# mysql.init_app(app)
# cursor = mysql.connect().cursor()

socketio = SocketIO(app)
CORS(app, origins="*")

online_users = set()
num_of_online_users = len(online_users)

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()

# try:
#     config = {
#     'user': os.getenv('DB_USER'),
#     'password': os.getenv('DB_PASSWORD'),
#     'host': os.getenv('DB_HOST'),
#     'database': os.getenv('DB_NAME')
# }

#     conn = connect(**config)
#     # cursor = conn.cursor()
#     print("Opened database successfully")
# except Error as e:
#     print(e)
#     pass

class GenderForm(FlaskForm):
    gender = SelectField('Gender', choices=['Male', 'Female', 'Other'])


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and session['logged_in']:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('landing'))
    return wrap



@login_required
@app.route('/', methods=['GET', 'POST'])
def landing():
    gender_choice = ['Male', 'Female', 'Other']
    gender_form = GenderForm()
    selected_option = ''
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        gender = request.form['gender']
        email = request.form['email']
        password = request.form['password']
        if selected_option == 'Male' or selected_option == 'Female' or selected_option == 'Other':

            return redirect(url_for('register'))
        return render_template('landing.html', gender_choice=gender_choice, selected_option=selected_option, gender_form=gender_form)
    return render_template('landing.html', gender_choice=gender_choice, selected_option=selected_option, gender_form=gender_form)

@app.route('/login', methods=['GET', 'POST'])

def login():
    gender_form = GenderForm()
    gender_choice = ['Male', 'Female', 'Other']
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            with app.app_context():
                query = f"SELECT * FROM users WHERE email='{email}'"
                cursor.execute(query)
                user = cursor.fetchone()

                if user and sha256_crypt.verify(password, user[5]):
                    session['user_id'] = user[0]
                    session['logged_in'] = True
                    session['email'] = user[4]
                    session['current_user'] = f"{user[1]} {user[2]}"
                    session['cookie'] = secrets.token_hex(16)
                    user = session['current_user']
                    return redirect(url_for('feed'))
                else:
                    flash("Invalid credentials")
                    return redirect(url_for('login'))
        except Error as e:
            print(e)
            pass
    return render_template('landing.html', gender_choice=gender_choice, gender_form=gender_form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    gender_form = GenderForm()
    gender_choice = ['Male', 'Female', 'Other']
    selected_option = ''
    try:
        if request.method == 'POST':
            fname = request.form['fname']
            lname = request.form['lname']
            gender = request.form['gender']
            email = request.form['email']
            password = request.form['password'] 
            phone_number = request.form['phone_number']

            print(fname, lname, gender, email, password)
            # database.insert_table(fname, lname, gender, email, sha256_crypt.hash(password), phone_number)
            with app.app_context():
                query = "INSERT into users (fname, lname, gender, email, password, phone_number) VALUES (?, ?, ?, ?, ?, ?)"
                
                cursor.execute(query, (fname, lname, gender, email, sha256_crypt.hash(password), phone_number))
                conn.commit()
                print("Records inserted successfully")
                return redirect(url_for('login'))
        else:
            flash("Invalid credentials")
            return redirect(url_for('register'))
    except Error as e:
        print(e)
        pass
    return render_template('landing.html', gender_choice=gender_choice, selected_option=selected_option, gender_form=gender_form)

@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    if request.method == 'POST':
        post = request.form['post']
        created_at = datetime.datetime.now()
        user_id = session['user_id']
        print(post, created_at, user_id)
        with app.app_context():
            query = "INSERT into posts (user_id, post_content, created_at) VALUES (?, ?, ?)" 
            cursor.execute(query, (user_id, post, created_at))
            conn.commit()
    return redirect(url_for('feed'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

@app.route('/albums')
@login_required
def albums():
    return render_template('albums.html')

@app.route('/birthdays')
@login_required
def birthdays():
    return render_template('birthdays.html')

@app.route('/blog-read')
@login_required
def blogread():
    return render_template('blog-read.html')

@app.route('/blogs')
@login_required
def blogs():
    return render_template('blogs.html')

@app.route('/chats-friend')
@login_required
def chatsfriend():
    return render_template('chats-friend.html')

@app.route('/chats-group')
@login_required
def chatsgroup():
    return render_template('chats-group.html')

@app.route('/course-intro')
@login_required
def courseintro():
    return render_template('course-intro.html')

@app.route('/courses')
@login_required
def courses():
    return render_template('courses.html')

@app.route('/create-group')
@login_required
def creategroup():
    return render_template('create-group.html')

@app.route('/create-page')
@login_required
def createpage():
    return render_template('create-page.html')

@app.route('/development-components')
@login_required
def developmentcomponents():
    return render_template('development-components.html')

@app.route('/development-icons')
@login_required
def developmenticons():
    return render_template('development-icons.html')

@app.route('/development-plugins')
@login_required
def developmentplugins():
    return render_template('development-plugins.html')

@app.route('/element')
@login_required
def element():
    return render_template('element.html')

@app.route('/events')
@login_required
def events():
    return render_template('events.html')

@app.route('/feed-layout2')
@login_required
def feedlayout2():
    return render_template('feedlayout2.html')

@app.route('/feed', methods=['GET', 'POST'])
@login_required
def feed():
    # user = None  # Initialize user to None or a default value
    user = session['current_user']
    if request.method == 'POST':
        post_id = request.form.get('post_id')
        posts = database.get_all_posts(conn=conn)

        comments_query = f"SELECT * FROM user_comments WHERE post_id={post_id}"
        cursor.execute(comments_query)
        comments = cursor.fetchall()
        print(comments)
        all_users_except_current_user = database.get_all_users(conn, session['user_id'])

    else:
        # Handle GET request or other methods if needed
        post_id = request.form.get('post_id')
        # print(post_id)
        posts = database.get_all_posts(conn=conn)
        all_users_except_current_user = database.get_all_users(conn, session['user_id'])
        # comments_query = f"SELECT * FROM user_comments WHERE post_id={post_id}"
        # cursor.execute(comments_query)
        # comments = cursor.fetchall()
        # print(comments)
        comments = []

    return render_template('feed.html', user=user, online_users=list(online_users), num_of_online_users=num_of_online_users, posts=posts, 
                           all_users_except_current_user=all_users_except_current_user, comments=comments)



@app.route('/post_comment', methods=['GET', 'POST'])
@login_required
def post_comment():
    if request.method == 'POST':
        print(request.form)
        user = session['current_user']
        user_email = session['email']
        post_id = request.form['post_id']
        comment = request.form['comments']
        created_at = datetime.datetime.now()
        parent_comment_id = None

        # print(user, user_email, post_id, comment, created_at)
        with app.app_context():
            try:
                database.comments(conn, session['user_id'], post_id, comment, 0, 0, parent_comment_id, created_at)
                return redirect(url_for('feed'))
            except Exception as e:
                print(e)
    return redirect(url_for('feed'))


@app.route('/form-login')
@login_required
def formlogin():
    return render_template('form-login.html')

@app.route('/form-register')
@login_required
def formregister():
    return render_template('form-register.html')

@app.route('/forums')
@login_required
def forums():
    return render_template('forums.html')

@app.route('/fundraiser')
@login_required
def fundraiser():
    return render_template('fundraiser.html')

@app.route('/games')
@login_required
def games():
    return render_template('games.html')

@app.route('/groups')
@login_required
def groups():
    return render_template('groups.html')

@app.route('/jobs', methods=['GET', 'POST'])
@login_required
def jobs():
    user = session['current_user']
    all_users_except_current_user = database.get_all_users(conn, session['user_id'])
    return render_template('jobs.html', user=user, online_users=list(online_users), num_of_online_users=num_of_online_users, all_users_except_current_user=all_users_except_current_user)

@app.route('/job-details')
@login_required
def jobdetails():
    return render_template('job-details.html')

@app.route('/pages-about')
@login_required
def pagesabout():
    return render_template('pages-about.html')

@app.route('/pages-contact')
@login_required
def pagescontact():
    return render_template('pages-contact.html')

@app.route('/pages-privacy')
@login_required
def pagesprivacy():
    return render_template('pages-privacy.html')

@app.route('/page-setting')
@login_required
def pagesetting():
    user = session['current_user']
    firstname = user.split()[0]
    lastname = user.split()[1]
    email = session['email']

    with app.app_context():
        query = "SELECT linkedin_profile, github_profile, about_user, user_location, working_at, job_title, experience, resume_url, website  FROM users WHERE email=?"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        linkedin_profile = result[0]
        github_profile = result[1]
        about_user = result[2]
        user_location = result[3]
        working_at = result[4]
        job_title = result[5]
        experience = result[6]
        resume = result[7]
        website = result[8]
        print(linkedin_profile, github_profile, about_user, user_location, working_at)
        return render_template('pages-setting.html', user=user, firstname=firstname, lastname=lastname, 
                            email=email, online_users=list(online_users), 
                            num_of_online_users=num_of_online_users,
                            linkedin_profile=linkedin_profile, github_profile=github_profile,
                            about_user=about_user, user_location=user_location, working_at=working_at,
                            job_title=job_title, experience=experience, resume=resume, website=website)

@app.route('/save_user_settings', methods=['GET', 'POST'])
@login_required
def save_user_settings():
    if request.method == 'POST':
        user = session['current_user']
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        linkedin_profile = request.form['linkedin_profile']
        github_profile = request.form['github_profile']
        about_user = request.form['about']
        user_location = request.form['location']
        working_at = request.form['working_at']
        job_title = request.form['job_title']
        experience = request.form['experience']
        resume = request.form['resume']
        website = request.form['website']

        print(fname, lname, email ,linkedin_profile, github_profile, about_user, user_location, working_at)
        try:
            with app.app_context():
                query = f"""UPDATE users SET fname='{fname}', lname='{lname}', email='{email}',
                linkedin_profile='{linkedin_profile}', github_profile='{github_profile}', about_user='{about_user}',
                    user_location='{user_location}', working_at='{working_at}', job_title='{job_title}', experience='{experience}',
                    resume_url='{resume}', website='{website}'
                    WHERE fname='{user.split()[0]}' AND lname='{user.split()[1]}'"""
                cursor.execute(query)
                conn.commit()
                session['current_user'] = f"{fname} {lname}"
                session['email'] = email
                return redirect(url_for('pagesetting'))
        except Error as e:
            print(e)
            pass
    return redirect(url_for('pagesetting'))

@app.route('/page-setting2')
@login_required
def pagesetting2():
    return render_template('pages-setting2.html')

@app.route('/pages-upgrade')
@login_required
def pagesupgrade():
    return render_template('pages-upgrade.html')

@app.route('/pages')
@login_required
def pages():
    return render_template('pages.html')

@app.route('/products')
@login_required
def products():
    return render_template('products.html')

@app.route('/product-single')
@login_required
def productsingle():
    return render_template('product-single.html')

@app.route('/timeline')
@login_required
def timeline():
    user = session['current_user']
    email = session['email']

    with app.app_context():
        posts = database.get_all_posts(conn=conn)
        query = "SELECT linkedin_profile, github_profile, about_user, user_location, working_at, job_title, experience, resume_url, website, about_user FROM users WHERE email=?"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        linkedin_profile = result[0]
        github_profile = result[1]
        about_user = result[2]
        user_location = result[3]
        working_at = result[4]
        job_title = result[5]
        experience = result[6]
        resume = result[7]
        website = result[8]
        about_user = result[9]
        
        return render_template('timeline.html', user=user, online_users=list(online_users), num_of_online_users=num_of_online_users, posts=posts,
                            linkedin_profile=linkedin_profile, github_profile=github_profile, user_location=user_location, working_at=working_at,
                            job_title=job_title, experience=experience, resume=resume, website=website, about_user=about_user)

@app.route('/timeline-event')
@login_required
def timelineevent():
    return render_template('timeline-event.html')

@app.route('/timeline-fundraiser')
@login_required
def timelinefundraiser():
    return render_template('timeline-fundraiser.html')

@app.route('/timeline-group')
@login_required
def timelinegroup():
    return render_template('timeline-group.html')

@app.route('/timeline-page')
@login_required
def timelinepage():
    return render_template('timeline-page.html')

@app.route('/videos')
@login_required
def videos():
    return render_template('videos.html')

@app.route('/video-watch')
@login_required
def videowatch():
    return render_template('video-watch.html')

@socketio.on('connect')
def handle_connect():
    user_id = session['user_id']
    if user_id:
        print(user_id)
        online_users.add(user_id)
    emit('online_users', list(online_users), broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    user_id = session['user_id']
    if user_id:
        online_users.discard(user_id)
    emit('online_users', list(online_users), broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
