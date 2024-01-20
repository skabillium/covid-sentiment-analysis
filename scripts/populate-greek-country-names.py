import sqlite3
import csv


conn = sqlite3.connect('db/vaccine-tweets.db')
cursor = conn.cursor()

with open('data/greek-country-names.csv', 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    for row in reader:
        greek_name, _, iso3 = row
        cursor.execute(
            'UPDATE country SET greek_name=? WHERE id=?', (greek_name, iso3))


conn.commit()
conn.close()
