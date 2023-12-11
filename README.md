# Python Machine Learning Powered Fan Sentiment App
- This repository is a flask project that models fan sentiment for the Philadelphia Union (Professional soccer team in the MLS)
This projects implements a custom trained nueral network for sentiment analysis. Tweets are scraped from twitter asynchronously and then 
analayzed for sentiment. The project also scrapes news story data for the Philadelphia Union, as well as Betting odds for the Union.
Then, it is aggregated on a front end interface

## You need:
- As of JULY 2023, the fan sentiment analysis part does not work. Elon Musk has shut down twitter scraping - This project utilizes the snscrape module, 
which is currently non-functional

## You need:
- Flask, Tensorflow, Snscrape Module, FlaskSQLALchemy
## Note:
- Scrapes twitter date by keyword for sports team sentiment and process through pretrained neural network to derive sentiment score
- Tracks scores in FLaskSQL db and compares with betting lines


## Installation
To install and run this project - install dependencies using npm and then start your server:

```
$ npm install
$ npm start
```

### live link:
- (https://www.kaoflow.com/)

### Some Dataset link for custom training:
- https://www.kaggle.com/datasets/tirendazacademy/fifa-world-cup-2022-tweets
