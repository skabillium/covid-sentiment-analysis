import requests
import csv
from bs4 import BeautifulSoup

url = 'https://el.wikipedia.org/wiki/ISO_3166-1'
response = requests.get(url)

if response.status_code != 200:
    print(f'Received non 200 response: {response}')

soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table', {'class': 'wikitable sortable'})

data = []
for row in table.find_all('tr'):
    name, _, iso3, iso2, _ = [cell.text.strip()
                              for cell in row.find_all(['td', 'th'])]
    data.append([name, iso2, iso3])


with open('data/greek-country-names.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(data)


print(f'Created file with {len(data) - 1} countries')
