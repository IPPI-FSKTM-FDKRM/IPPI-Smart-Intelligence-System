from flask import Flask, render_template, url_for, redirect

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from key import *
from SocialMediaProfiler import app, celery, insta



@app.route("/insta/search")
@login_required
def instaSearch():
    return render_template("insta-search.html")

@app.route("/insta/search")
@login_required
def instaSearchResult(word=None):
    profile = insta.user_search(word)
    return render_template("insta-search.html", result=profile)

@app.route("/insta/profile/<id>")
@login_required
def instaProfile(id):
    try:
        profile = insta.user_profile(id)
        media = insta.user_media(id)
        return render_template("insta-profile.html", user=profile, media=media)
    except Exception as e:
        return render_template("insta-private.html", error = e)

