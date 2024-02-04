"""
Export geojson file containing for each country:
- Country name
- Polygons to draw it on a map
- Total tweet count
- Percentages for positive, neutral and negative sentiments
"""

import sqlite3
import json
import sqlite3


SQLITE_DB = 'db/vaccine-tweets.db'

conn = sqlite3.connect(SQLITE_DB)
cursor = conn.cursor()

tweet_geoson = {
    'type': 'FeatureCollection',
    'features': []
}


with open('data/countries.geojson', 'r') as file:
    countries = json.load(file)['features']

for country in countries:
    name = country['properties']['ADMIN']
    iso3 = country['properties']['ISO_A3']

    if iso3 == '-99':
        continue

    cursor.execute('SELECT name, greek_name, flag_url, vaccine_coverage FROM country WHERE id=?',
                   (iso3,))

    country_row = cursor.fetchone()
    if country_row is None:
        continue

    name, greek_name, flag_url, vaccine_coverage = country_row

    cursor.execute("""
    SELECT
        COUNT(*) AS tweet_count,
        SUM(CASE WHEN vader_score > 0 THEN 1 ELSE 0 END) AS positive_count,
        SUM(CASE WHEN vader_score = 0 THEN 1 ELSE 0 END) AS neutral_count,
        SUM(CASE WHEN vader_score < 0 THEN 1 ELSE 0 END) AS negative_count
    FROM tweet
    WHERE country_id = ?
    """, (iso3,))

    tweet_count, positive, neutral, negative = cursor.fetchone()
    if tweet_count < 50:
        continue

    country['properties']['greekName'] = greek_name
    country['properties']['flagUrl'] = flag_url
    country['properties']['positivePct'] = round(positive/tweet_count*100, 1)
    country['properties']['neutralPct'] = round(neutral/tweet_count*100, 1)
    country['properties']['negativePct'] = round(negative/tweet_count*100, 1)
    country['properties']['vaccineCoverage'] = round(vaccine_coverage, 1)
    country['properties']['tweets'] = tweet_count
    tweet_geoson['features'].append(country)


conn.commit()
conn.close()

with open('data/tweets.geojson', 'w') as file:
    file.write(json.dumps(tweet_geoson))
