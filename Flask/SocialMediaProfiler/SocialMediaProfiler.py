from celery import Celery
import Facebook , Instagram, Twitter
import os
import pytz
from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_googlemaps import GoogleMaps
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from instagram.client import InstagramAPI
from werkzeug.security import generate_password_hash, check_password_hash

from config import *
from forms import LoginForm, RegisterForm

from flask import render_template, jsonify, request
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
app.config['GOOGLEMAPS_KEY'] = GOOGLEKEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/kayd/Project/IPPI-Smart-Intelligence-System/Flask/SocialMediaProfiler/database.db' #linux

GoogleMaps(app)
# "C:\Users\user\Project\IPPI-Smart-Intelligence-System\Flask\SocialMediaProfiler\database.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\nurfirdaus\\Documents\\GitHub\\IPPI-Smart-Intelligence-System\\Flask\\SocialMediaProfiler\\database.db' #windows
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\user\\Project\\IPPI-Smart-Intelligence-System\\Flask\\SocialMediaProfiler\\database.db' #windows


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\User\\PycharmProjects\\untitled1\\database.db' #windows #raam

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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
@login_required
def index():
    user = current_user.username
    return render_template("Home.html", user = user)

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
    form = RegisterForm()

    if form.validate_on_submit():
        hash_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hash_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1> New User has been created!</h1>'

    return render_template("register.html", form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/searchGeneral")
@login_required
def searchGeneral():
    return render_template("searchGeneral.html")
