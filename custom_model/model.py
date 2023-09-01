import tensorflow as tf
from tensorflow.keras import Sequential,layers,regularizers
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Dense,Input,Bidirectional,LSTM
from sklearn.utils import shuffle
import tensorflow_hub as hub
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
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


DATASET_ENCODING = "ISO-8859-1"
print('STARTING')


df = pd.read_csv("archive.zip",encoding=DATASET_ENCODING)
df= df.iloc[:,[0,-1]]
df.columns = ['sentiment','tweet']
df = pd.concat([df.query("sentiment==0").sample(50000),df.query("sentiment==4").sample(50000)])
df.sentiment = df.sentiment.map({0:0,4:1})
df =  shuffle(df).reset_index(drop=True)

df,df_test = train_test_split(df,test_size=0.2)

print(df.head(10))
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

print("LOADED HUB")

embed(['hi samuels, this is our project']).numpy().shape

def vectorize(df):
    embeded_tweets = embed(df['tweet'].values.tolist()).numpy()
    targets = df.sentiment.values
    return embeded_tweets,targets

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


df['tweet'] = df['tweet'].apply((lambda x: process_tweets(x)))
print(df.head(10))
print("Beginning Embedding")
embeded_tweets,targets = vectorize(df)

model = Sequential()
model.add(Input(shape=(512,),dtype='float32'))
model.add(Dense(128, activation = 'relu'))
model.add(Dense(64, activation = 'relu'))
model.add(Dense(1, activation = 'sigmoid'))
print("IN PROGRESS CHECK 1")
model.compile(loss='binary_crossentropy', 
              optimizer='adam',
              metrics=['acc'])

model.summary()

num_epochs = 6
batch_size = 64   ## 2^x

history = model.fit(embeded_tweets, 
                    targets, 
                    epochs=num_epochs, 
                    validation_split=0.1, 
                    batch_size=batch_size)

df_test['tweet'] = df_test['tweet'].apply((lambda x: process_tweets(x)))
embed_test,targets = vectorize(df_test)
predictions = np.round(model.predict(embed_test)).astype(int)
print(predictions[0:100])
print(accuracy_score(predictions,targets)*100)

model.save('saved_model/my_model')