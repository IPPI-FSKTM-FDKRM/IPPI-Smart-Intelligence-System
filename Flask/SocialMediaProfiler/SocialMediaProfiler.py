from celery import Celery
import Facebook , Instagram, Twitter
import os
import pytz
from flask import Flask, render_template, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from flask_googlemaps import GoogleMaps
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from instagram.client import InstagramAPI
from werkzeug.security import generate_password_hash, check_password_hash

from config import *
from forms import *

from flask import render_template, jsonify, request
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
app.config['GOOGLEMAPS_KEY'] = GOOGLEKEY
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/kayd/Project/IPPI-Smart-Intelligence-System/Flask/SocialMediaProfiler/database.db' #linux

GoogleMaps(app)
# "C:\Users\user\Project\IPPI-Smart-Intelligence-System\Flask\SocialMediaProfiler\database.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\nurfirdaus\\Documents\\GitHub\\IPPI-Smart-Intelligence-System\\Flask\\SocialMediaProfiler\\database.db' #windows
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\user\\Project\\IPPI-Smart-Intelligence-System\\Flask\\SocialMediaProfiler\\database.db' #windows

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/User/Documents/GitHub/IPPI-Smart-Intelligence-System/Flask/SocialMediaProfiler/database.db' #linux raam

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\User\\Documents\\GitHub\\IPPI-Smart-Intelligence-System\\Flask\\SocialMediaProfiler\\database.db' #windows #raam

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

fb = Facebook.Facebook()
insta = Instagram.Instagram()
twitter = Twitter.Twitter()

from FacebookView import *
from InstagramView import *
from TwitterView import *


if __name__ == '__main__':
    app.run()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
@login_required
def index():
    first = current_user.first_name
    last = current_user.last_name
    email = current_user.email
    username = current_user.username
    return render_template("Home.html", first = first, last = last, email = email, username = username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error=''
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('index'))

        error = 'Invalid username or password'
        return render_template("login.html", form=form, error=error)

    return render_template("login.html", form = form, error = error)

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    error = ''
    if User.query.filter_by(username='admin').first():

        form = RegisterForm()

        if form.validate_on_submit():
            hash_password = generate_password_hash(form.password.data, method='sha256')
            if User.query.filter_by(username=form.username.data).first():
                error = 'Username has been taken'
                return render_template("register.html", form=form, error=error)
            elif User.query.filter_by(email=form.email.data).first():
                error = 'Email has been used'
                return render_template("register.html", form=form, error=error)
            else:
                new_user = User(username=form.username.data, email=form.email.data, password=hash_password, first_name=form.first_name.data, last_name=form.last_name.data)
                db.session.add(new_user)
                db.session.commit()

                message = 'New User has been created!'
                return render_template("success_register.html", message = message)


        return render_template("register.html", form = form)

    else:

        return render_template("404.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/searchGeneral")
@login_required
def searchGeneral():
    return render_template("searchGeneral.html")

@app.route('/userProfile')
@login_required
def userProfile():
    first = current_user.first_name
    last = current_user.last_name
    email = current_user.email
    username = current_user.username

    return render_template("userProfile.html", first=first, last=last, email=email, username=username)

@app.route('/changePassword', methods=['GET', 'POST'])
@login_required
def changePassword():
    form = ChangePassword()

    if form.validate_on_submit():
        hash_password = generate_password_hash(form.password1.data, method='sha256')
        user = current_user
        user = current_user
        user.password = hash_password
        db.session.add(user)
        db.session.commit()
        flash('Password has been updated!', 'success')
        return redirect(url_for('userProfile'))

    return render_template('password_change.html', form=form)