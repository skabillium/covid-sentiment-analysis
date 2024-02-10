import json
import sqlite3
import pandas as pd

conn = sqlite3.connect('db/vaccine-tweets.db')

non_negative_query = """
SELECT
    t.country_id,
    COUNT(*) AS total_tweets,
    SUM(CASE WHEN t.vader_score > 0 THEN 1 ELSE 0 END) AS positive_count,
    SUM(CASE WHEN t.vader_score = 0 THEN 1 ELSE 0 END) AS neutral_count,
    c.vaccinated_at_nov2021 as vaccine_coverage
FROM tweet t JOIN country c ON t.country_id=c.id
GROUP BY t.country_id
"""

df = pd.read_sql_query(non_negative_query, conn)
conn.close()


df['non_negative_pct'] = (df['positive_count'] +
                          df['neutral_count']) / df['total_tweets']


results = {}
results['pearson'] = df['non_negative_pct'].corr(
    df['vaccine_coverage'], method='pearson')
results['kendall'] = df['non_negative_pct'].corr(
    df['vaccine_coverage'], method='kendall')
results['spearman'] = df['non_negative_pct'].corr(
    df['vaccine_coverage'], method='spearman')
results['compound'] = (results['pearson'] +
                       results['kendall'] + results['spearman']) / 3


with open('data/correlation.json', 'w') as f:
    json.dump(results, f, indent=4)
