import snscrape.modules.twitter as sntwitter
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense,Input
from sklearn.utils import shuffle
import tensorflow_hub as hub
import numpy as np
import os
import pandas as pd
from sklearn.metrics import accuracy_score
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string


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



scraper = sntwitter.TwitterSearchScraper("Philadelphia Union")

model = tf.keras.models.load_model('saved_model/my_model')
model.summary()

embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

tweets = []

for i,tweet in enumerate(scraper.get_items()):
    tweet = process_tweets(tweet.content)
    tweets.append(tweet)
    if i > 50:
        break

embedded_tweets = embed(tweets).numpy()

predictions = model.predict(embedded_tweets).astype(float)
