"""
Initalize the database for with tables "country" and "tweet"
"""
import os
import sqlite3


# If database directory and file are not found, create them
database_dir = 'db'
database_file = database_dir + '/vaccine-tweets.db'

if not os.path.exists(database_dir):
    os.makedirs(database_dir)
    print(f'Created directory {database_dir}')

if not os.path.exists(database_file):
    with open(database_file, 'w') as file:
        print(f'Created file {database_file}')
        pass


conn = sqlite3.connect(database_file)
cursor = conn.cursor()


# Create countries table
cursor.execute("""
CREATE TABLE IF NOT EXISTS country (
    id TEXT PRIMARY KEY, -- id is aplha-3 ISO code
    name TEXT,
    greek_name TEXT,
    iso2 TEXT,
    flag_url TEXT,
    continent TEXT,
    vaccine_coverage REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tweet (
    id INTEGER PRIMARY KEY,
    user_name TEXT,
    user_location TEXT,
    user_description TEXT,
    user_created TEXT,
    user_followers INTEGER,
    user_friends INTEGER,
    user_favourites INTEGER,
    user_verified INTEGER,
    date TEXT,
    text TEXT,
    hashtags TEXT,
    source TEXT,
    retweets INTEGER,
    favorites INTEGER,
    is_retweet INTEGER,
    vader_score REAL,
    textblob_score REAL,
    country_id TEXT,
    FOREIGN KEY (country_id) REFERENCES country(id)
);
""")

print('Created tables country & tweet')

conn.commit()
conn.close()
