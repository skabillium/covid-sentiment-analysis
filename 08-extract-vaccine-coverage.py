"""
Extract the vaccine coverage for each country up until 2021-11-30 (The end of our tweet dataset).
This script uses data from the World Health Organization.
"""
import pandas as pd
import sqlite3

df = pd.read_csv('data/who-covid.csv')

# Get the vaccination percentages up until the end of 2021
df = df[df['date'] == '2021-11-30'][['iso_code',
                                     'location', 'date', 'people_vaccinated_per_hundred']].dropna().sort_values('people_vaccinated_per_hundred', ascending=False)


conn = sqlite3.connect('db/vaccine-tweets.db')
cursor = conn.cursor()

for _, country in df.iterrows():
    cursor.execute('UPDATE country SET vaccine_coverage=? WHERE id=?',
                   (country['people_vaccinated_per_hundred'], country['iso_code']))


conn.commit()
conn.close()
