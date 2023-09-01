import requests
import json
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from statistics import mean 
import asyncio
from datetime import datetime, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import Team, app, db
import snscrape.modules.twitter as sntwitter
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense,Input
import tensorflow_hub as hub
import numpy as np
import os
import pandas as pd
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string, time

key = "Philadelphia Union"

nltk.download('stopwords')
stopword = set(stopwords.words('english'))
nltk.download('punkt')
nltk.download('wordnet')


def process_tweets(tweet):
  # Lower Casing
    urlPattern = r"((http://)[^ ]*|(https://)[^ ]*|( www\.)[^ ]*)"
    userPattern = '@[^\s]+'
    tweet = tweet.lower()
    # Removing all URls 
    tweet = re.sub(urlPattern,'',tweet)
    # Removing all @username.
    tweet = re.sub(userPattern,'', tweet) 
    #Remove punctuations
    tweet = tweet.translate(str.maketrans("","",string.punctuation))
    #tokenizing words
    tokens = word_tokenize(tweet)
    #Removing Stop Words
    final_tokens = [w for w in tokens if w not in stopword]
    #reducing a word to its word stem 
    wordLemm = WordNetLemmatizer()
    finalwords=[]
    for w in final_tokens:
        if len(w)>1:
            word = wordLemm.lemmatize(w)
            finalwords.append(word)
    return ' '.join(finalwords)

async def main():
    model = tf.keras.models.load_model('saved_model/my_model')
    model.summary()
    embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
    scraper = sntwitter.TwitterSearchScraper(key)
    tweets = []
    for i,tweet in enumerate(scraper.get_items()):
        tweet = process_tweets(tweet.content)
        tweets.append(tweet)
        if i > 50:
            break
    embedded_tweets = embed(tweets).numpy()
    predictions = model.predict(embedded_tweets).astype(float)
    score = np.mean(predictions) * 100
    print(score)
    team = Team(team=key, sentiment=score, time=datetime.now())
    db.session.add(team)
    db.session.commit()
    time.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())


