from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests, time
import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import Articles, app, db
from datetime import datetime
import pytz 

# specify url to scrape



url = 'https://news.google.com/search?q=philadelphia%20union%20when%3A2d&hl=en-US&gl=US&ceid=US%3Aen'
    # alternative-1 (online parsing)
page = requests.get(url).text

# create an object to scrape various data later
soup = BeautifulSoup(page, 'html.parser')
#title
result_tl = soup.select('article .DY5T1d.RZIKme')
title = [t.text for t in result_tl]

#date-time
result_dt = soup.select('[datetime]')
timedate = [d['datetime'] for d in result_dt]

result_src = soup.select('article .wEwyrc')
source = [s.text for s in result_src]
links = []
# let's turn all relative-url into absolute-url by iterating all links
base_url = 'https://news.google.com/'
for i in soup.select('article .DY5T1d.RZIKme'):
    ss = urljoin(base_url, i.get('href'))
    # put all absolute links into empty list
    links.append(ss)
# putting all of data into a list
all_data = list(zip(title, timedate, links))
est = pytz.timezone('US/Eastern')
for i,article in enumerate(all_data):
    date_obj = datetime.strptime(timedate[i], '%Y-%m-%dT%H:%M:%SZ')
    est_time = date_obj.astimezone(est)
    exists = Articles.query.filter_by(title=title[i]).first()
    if not exists:
        article = Articles(title=title[i], link=links[i], time=est_time.strftime('%m-%d  %H:%M'), source=source[i])
        db.session.add(article)
    db.session.commit()
    if i>15:
        break