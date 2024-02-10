"""Copy images and geojson file to /web"""

import shutil


# Images
shutil.copy2('images/monthly-sentiment-split.png',
             'web/public/monthly-sentiment-split.png')
shutil.copy2('images/monthly-tweet-distribution.png',
             'web/public/monthly-tweet-distribution.png')

shutil.copy2('data/tweets.geojson', 'web/src/tweets.json')


print('Copied images and assets to "web"')
