"""Extract location data from tweets"""


import sqlite3
import pandas as pd


US_STATES_FILE = 'data/us-states.csv'
SQLITE_DB = 'db/vaccine-tweets.db'


conn = sqlite3.connect(SQLITE_DB)
cursor = conn.cursor()

tweets = pd.read_sql_query(
    'SELECT * FROM tweet WHERE user_location IS NOT NULL', conn)
print(f'Found {len(tweets)} tweets with known location')

us_states = pd.read_csv(US_STATES_FILE)


def add_country_to_tweets(cursor: sqlite3.Cursor, tweets: pd.DataFrame):
    for _, row in tweets.iterrows():
        cursor.execute("""
        UPDATE tweet SET country_id=? WHERE id=?
""", (row['country_id'], row['id']))


# Special query for the US & UK since twitter's location records state data
american = tweets[tweets['user_location'].str.contains(
    '|'.join(['US', 'USA', 'America', 'United States', 'United States of America'])) | tweets['user_location'].str.contains('|'.join([*us_states['State'].values.tolist(), *us_states['Abbreviation'].values.tolist()]))]
american['country_id'] = 'USA'
add_country_to_tweets(cursor=cursor, tweets=american)
print(f'Found {len(american)} tweets from USA')


AdditionalTerms = {
    'GRC': ['Greece', 'greek', 'hellas', 'athens', 'thessaloniki'],
    'CYP': ['Cyprus', 'cypriot', 'nicosia'],
    'IND': ['India', 'hindu', 'bharat'],
    'GBR': ['United Kingdom', 'great britain', 'england', 'london', 'birmingham', 'wolverhampton', 'scotland', 'glasgow', 'edinburgh', 'wales', 'northern ireland'],
    'FRA': ['France', 'paris'],
    'DEU': ['Germany', 'german', 'berlin', 'hamburg', 'munich', 'münchen', 'Cologne', 'köln', 'frankfurt']
}


for _id in AdditionalTerms.keys():
    terms = AdditionalTerms[_id]
    query = '|'.join(terms)
    frame = tweets[tweets['user_location'].str.contains(
        query, case=False) | tweets['hashtags'].str.contains(query, case=False)]
    frame['country_id'] = _id
    add_country_to_tweets(cursor=cursor, tweets=frame)
    print(f'Found {len(frame)} tweets from {terms[0]}')

cursor.execute("""
    SELECT country.id, country.name FROM country LEFT JOIN tweet ON country.id=tweet.country_id
    WHERE tweet.country_id IS NULL
""")
countries = cursor.fetchall()[1:]
for country in countries:
    _id, name = country
    cursor.execute("""
UPDATE tweet SET country_id=? WHERE user_location LIKE ? COLLATE NOCASE
""", (_id, f'%{name}%'))
    print(f'Found {cursor.rowcount} tweets from {name}')


conn.commit()
conn.close()
