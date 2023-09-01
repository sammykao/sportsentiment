from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import Fixture, Line, app, db
from datetime import datetime, timedelta
import requests, time
import pytz 

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

querystring = {"season":"2023","team":"1599","next":"3"}

headers = {
    "X-RapidAPI-Key": "29ae4b4449msheeedd0d1a66531cp1a2786jsnd2153dc0215b",
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}
response = requests.get(url, headers=headers, params=querystring).json()


est = pytz.timezone('US/Eastern')

for i,fixture in enumerate(response['response']):
    event = f"{fixture['teams']['home']['name']} (Home) vs. {fixture['teams']['away']['name']} (Away)"
    if fixture['teams']['home']['name'] == "Philadelphia Union":
        home_or_away = 0
    else:
        home_or_away = 1
    status = fixture['fixture']['status']['short']
    matchtime = fixture['fixture']['date']
    date_obj = datetime.strptime(matchtime, '%Y-%m-%dT%H:%M:%SZ')
    est_time = date_obj.astimezone(est)
    db_fixture = Fixture(event=event, matchtime=est_time.strftime('%m-%d  %H:%M'))
    db.session.add(db_fixture)
    db.session.commit()
    if i == 0:
        if status == 'NS':
            new_url = "https://api-football-v1.p.rapidapi.com/v3/odds"
        else:
            new_url = "https://api-football-v1.p.rapidapi.com/v3/odds/live"
        querystring = {"fixture":fixture['fixture']['id']} 
        new_reponse = requests.get(new_url, headers=headers, params=querystring).json()
        moneyline = new_reponse['response'][0]['bookmakers'][4]['bets'][0]['values'][home_or_away]['odd']
        line = Line(event=event, moneyline=((1/float(moneyline)) * 100), time=(datetime.now() - timedelta(hours=4)))
        db.session.add(line)
        db.session.commit()


