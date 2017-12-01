from flask import Flask, render_template, url_for, redirect, jsonify, request
import json
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from config import *
from SocialMediaProfiler import app, celery, insta



@app.route("/insta/search")
@login_required
def instaSearch():
    return render_template("insta-search.html")

@app.route("/insta/search/result", methods = ["POST"])
@login_required
def instaSearchResult():
    print "danish"
    data = json.loads(request.data)
    profile = insta.user_search(data)
    print profile
    #return render_template("insta-search.html", result=profile)
    return jsonify({'result': render_template("insta-search-result.html", result=profile)})

@app.route("/insta/profile/<id>")
@login_required
def instaProfile(id):
    try:
        profile = insta.user_profile(id)
        media = insta.user_media(id)
        return render_template("insta-profile.html", user=profile, media=media)
    except Exception as e:
        return render_template("insta-private.html", error = e)
