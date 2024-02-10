"""
Export images displaying:
1. Monthly tweet count distribution
2. Monthly sentiment distribution
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


def save_monthly_count_distribution_image(df: pd.DataFrame):
    """Display tweet distribution by month"""
    # Extract month and year
    df['month'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m')

    # Group data by month, count occurrences
    monthly_distribution = df['month'].value_counts().sort_index()
    monthly_distribution.index = pd.to_datetime(monthly_distribution.index,
                                                format='%Y-%m').strftime('%b %Y')

    min_month = pd.to_datetime(df['month']).min().strftime('%B %Y')
    max_month = pd.to_datetime(df['month']).max().strftime('%B %Y')

    # Create a bar plot
    plt.figure(figsize=(12, 6))
    monthly_distribution.plot(kind='bar', color='skyblue')
    plt.xlabel('Month')
    plt.ylabel('Tweets')
    plt.title(f'Distribution by Month ({min_month} to {max_month})')
    plt.xticks(rotation=45)
    plt.savefig('images/monthly-tweet-distribution.png')


def save_monthly_sentiment_distribution_image(df: pd.DataFrame):
    """Display bar chart with sentiment split per month"""
    df['date'] = pd.to_datetime(df['date'])
    df['value_category'] = pd.cut(df['vader_score'], bins=[-float('inf'),
                                  0, float('inf')], labels=['negative', 'positive'], right=False)

    df['value_category'] = pd.cut(df['vader_score'], bins=[-float('inf'), 0, 0.01, float(
        'inf')], labels=['negative', 'neutral', 'positive'], right=False)

    # Group by month and 'value_category', count occurrences, and unstack
    grouped_df = df.groupby([df['date'].dt.to_period(
        'M'), 'value_category']).size().unstack(fill_value=0)

    grouped_df.sort_index(level=0)
    grouped_df.index = grouped_df.index.strftime('%b %Y')

    colors = {
        'negative': '#92013A',
        'positive': '#00429C',
        'neutral': '#FFCAB9'
    }

    # Plot the bar chart
    grouped_df.plot(kind='bar', stacked=True, color=[
                    colors[col] for col in grouped_df.columns])
    plt.title('Sentiment split grouped by month')
    plt.xlabel('Month')
    plt.ylabel('Tweets')
    plt.legend(title='Sentiment score')
    plt.savefig('images/monthly-sentiment-split.png')


def save_non_negative_sentiment_to_coverage_image(conn: sqlite3.Connection):
    """Create an image with a scatter plot of non-negative sentiment to vaccine coverage per country"""
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
    df['non_negative_pct'] = (df['positive_count'] +
                              df['neutral_count']) / df['total_tweets']

    _, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df['non_negative_pct'], df['vaccine_coverage'],
               color='blue', alpha=0.7)

    ax.set_xlabel('Sentiment Percentage')
    ax.set_ylabel('Vaccine Coverage')
    plt.title('Sentiment vs Vaccine Coverage per Country')

    plt.savefig('images/sentiment-to-coverage.png')


conn = sqlite3.connect('db/vaccine-tweets.db')

tweets = pd.read_sql_query('SELECT vader_score, date FROM tweet', conn)

save_monthly_count_distribution_image(tweets)
save_monthly_sentiment_distribution_image(tweets)
save_non_negative_sentiment_to_coverage_image(conn)
