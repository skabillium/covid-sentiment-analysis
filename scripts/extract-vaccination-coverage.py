
import pandas as pd

df = pd.read_csv('data/who-covid.csv')

# Get the vaccination percentages up until the end of 2021
df = df[df['date'] == '2021-11-30'][['iso_code',
                                     'location',  'people_vaccinated_per_hundred']].dropna()


df.to_csv('data/who-vaccine-coverage.csv', index=False)
