from datetime import datetime, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sentiment.db'
db = SQLAlchemy(app)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String(200), nullable=False)
    sentiment = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now)

class Line(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String, nullable=False)
    moneyline = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now)

class Fixture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String, nullable=False)
    matchtime = db.Column(db.String, nullable=False)

class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    source = db.Column(db.String, nullable=False)



app.app_context().push()
db.create_all()

