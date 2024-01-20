"""Score every text as positive, neutral or negative using 2 models: VADER & TextBlob"""

import re
import sqlite3
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob


def preprocess(text: str) -> str:
    """Remove hashtags, tags & urls"""
    text = re.sub(r'#\w+', '', text)  # Remove hashtags
    text = re.sub(r'@\w+', '', text)  # Remove tags
    text = re.sub(r'http\S+|www\S+', '', text)  # Remove URLs
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text


conn = sqlite3.connect('db/vaccine-tweets.db')
cursor = conn.cursor()

vader = SentimentIntensityAnalyzer()

tweets = pd.read_sql_query('SELECT id, text FROM tweet', conn)

print(f'Scoring {len(tweets)} tweets...')
for _, tweet in tweets.iterrows():
    cursor.execute("""
UPDATE tweet SET vader_score=?, textblob_score=? WHERE id=?
""", (vader.polarity_scores(preprocess(tweet['text']))['compound'], TextBlob(preprocess(tweet['text'])).sentiment.polarity, tweet['id']))


conn.commit()
conn.close()
