from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import Team, Line, Fixture, Articles, app, db
from news import newsrun
from apscheduler.schedulers.background import BackgroundScheduler
from fixturelines import linesrun


scheduler = BackgroundScheduler()
scheduler.add_job(func=linesrun, trigger="interval", minutes=30)
scheduler.start()

sched = BackgroundScheduler()
sched.add_job(func=newsrun, trigger="interval", minutes=10)
sched.start()


@app.route('/') 
def index():
        fixtures = Fixture.query.order_by(Fixture.id.desc()).limit(3)
        fixtures = fixtures[::-1]
        kwargs = { 'event' : fixtures[0].event }
        lines = Line.query.filter_by(**kwargs).order_by(Line.id.desc()).limit(8).all()
        lines = lines[::-1]
        teams = Team.query.order_by(Team.time.desc()).limit(25).all()
        teams = teams[::-1]
        sent_times = []
        sent_scores = []
        line_times = []
        line_odds = []
        for team in teams:
            sent_times.append(team.time.strftime("%I:%M"))
            sent_scores.append("{:.2f}".format(team.sentiment))
        for line in lines:
            line_times.append(line.time.strftime("%I:%M"))
            line_odds.append(line.moneyline)
        articles = Articles.query.order_by(Articles.id.desc()).limit(15)
        articles = articles[::-1]
        return render_template('index.html', articles=articles, sent_times=sent_times, sent_scores=sent_scores, fixtures=fixtures, line_times=line_times, line_odds=line_odds )
if __name__ == "__main__":  
    app.run(debug=True)