from celery import Celery
from flask import Flask , blueprints
from flask_googlemaps import GoogleMaps
from FacebookModule import Facebook

from flask import render_template, jsonify, request

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
app.config['GOOGLEMAPS_KEY'] = "AIzaSyCQaXdeh30YGYlYPK6eqt9AcAJC4or5I8w"
GoogleMaps(app)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

fb = Facebook.Facebook()

from FacebookModule.FacebookView import fbBP






if __name__ == '__main__':
    app.run()


app.register_blueprint(fbBP, url_prefix="/facebook")


@app.route("/")
def index():
    return render_template("Home.html")
