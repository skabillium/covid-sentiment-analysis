"""Populate tables with tweets and countries"""

import sqlite3
import pandas as pd

countries = pd.read_csv('data/countries.csv')
gr = pd.read_csv('data/greek-country-names.csv')


countries = pd.merge(countries, gr, left_on='id',
                     right_on='alpha-3', how='left').drop(['alpha-3', 'alpha-2'], axis=1)


conn = sqlite3.connect('db/vaccine-tweets.db')

countries.to_sql('country', conn, index=False, if_exists='append')
print(f'Inserted {len(countries)} countries to the database')


tweets = pd.read_csv('data/vaccine-tweets.csv')
tweets.to_sql('tweet', conn, index=False, if_exists='append')
print(f'Inserted {len(tweets)} tweets to the database')

conn.close()
