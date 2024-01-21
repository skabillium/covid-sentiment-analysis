# Covid-19 Tweets Sentiment Analysis

This is the repo for my Master's Thesis at Computer engineering and Informatics department at the 
University of Patras. The purpose of this thesis is to evaluate the sentiment of Covid-19 vaccine
related tweets, compare different countries & display the result in a web interface.

## Requirements
To run this project you will need the following:
- [Python](https://www.python.org/downloads/) 3.9
- [Pip](https://pypi.org/project/pip/) 21
- [Nodejs](https://nodejs.org/en) 18+
- [Pnpm](https://pnpm.io/installation#compatibility) 8

To install the dependencies for the data pipeline it is recommended to use `venv`
```sh
pip install venv
pip -m venv .venv
source .venv/bin/activate

# Install dependencies
pip -r requirements.txt
```

## Dataset
The dataset contains approximatelly 230.000 tweets posted from December 2020 up until November 2021.
It was gathered by web scraping Twitter and extracting the tweets that mention Covid-19 vaccines.


## Overview
The project consists of 2 major parts: the data pipeline and the web interface. Each file starting
with a number `x-name-of-script.py` is a part of the pipeline and handles exactly one step of it.
To run the entire pipeline you can run the `pipeline-runner.py` script. This will:
1. Create the database file and initialize the schema
2. Populate the database with countries and tweets
3. Extract location data from every tweet possible
4. Calculate the most popular hashtags and save them to a file
5. Analyze the sentiment of every tweet in the database
6. Export some images for sentiment split per month and tweet count ditribution
7. Create the `.geojson` file for the web interface
8. Extract the vaccine coverage as of November 2021 per country
9. Copy images and `.geojson` files to the `/web` directory

After all that you can navigate to the `/web` directory, install the dependencies and run the project:
```sh
cd web
pnpm install
pnpm run dev
```

## Data files
Some files like `vaccine-tweets.csv` were larger than the allowed limits of github so if you want to
reproduce this project locally you can send me a email at [skabillium@gmail.com](mailto:skabillium@gmail.com)