"""Extract popular hashtags from tweet dataset"""

import sqlite3
import pandas as pd

conn = sqlite3.connect('db/vaccine-tweets.db')

tweets = pd.read_sql_query(
    'SELECT hashtags FROM tweet WHERE hashtags IS NOT NULL', conn)

tweets['hashtags'] = tweets['hashtags'].apply(lambda x: eval(x))

hashtag_series = tweets['hashtags'].explode().str.lower()

hashtags_count = hashtag_series.value_counts()

top = 50
popular = hashtags_count.head(top)

# HASTAGS_CSV = 'data/50-popular-hashtags.csv'
# popular.to_csv(HASTAGS_CSV)

popular.to_sql('hashtag', conn, if_exists='append')


# print(f'Saved {top} most popular hashtags to {HASTAGS_CSV}')
