from flask import Flask, render_template, request, redirect, url_for, flash, session
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

load_dotenv()


config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME')
}

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['FLASK_ENV'] = 'development'
app.config['DEBUG'] = True
app.config['FLASK_APP'] = 'app.py'
CORS(app, origins="*")
conn = connect(**config)
cursor = conn.cursor()

class GenderForm(FlaskForm):
    gender = SelectField('Gender', choices=['Male', 'Female', 'Other'])
# @app.route('/')
# def index():
#     return render_template('index.html')

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

        print(fname, lname, gender, email, password)
        if selected_option == 'Male' or selected_option == 'Female' or selected_option == 'Other':
            print(fname, lname, gender, email, password)
        return render_template('landing.html', gender_choice=gender_choice, selected_option=selected_option, gender_form=gender_form)
    return render_template('landing.html', gender_choice=gender_choice, selected_option=selected_option, gender_form=gender_form)

@app.route('/login', methods=['GET', 'POST'])

def login():
    gender_form = GenderForm()
    gender_choice = ['Male', 'Female', 'Other']
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

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

            query = "INSERT into users (fname, lname, gender, email, password, phone_number) VALUES (%s, %s, %s, %s, %s, %s)"
            
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
    user = session['current_user']
    return render_template('feed.html', user=user)

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
    return render_template('jobs.html')

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
    return render_template('pages-setting.html', user=user, firstname=firstname, lastname=lastname, email=email)

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
    return render_template('timeline.html', user=user)

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



if __name__ == '__main__':
    app.run(debug=True)