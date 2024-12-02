import streamlit as st
import feedparser
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
from collections import Counter
import re
import schedule  # Added for scheduling
import time  # Added for scheduling
import threading  # Added for threading

# Function to fetch and parse RSS feeds
def fetch_feed(url):
    return feedparser.parse(url)

# Function to update the RSS feeds periodically
def update_feeds():  # New function for periodic updates
    global all_entries
    all_entries = []
    for i, url in enumerate(rss_feeds):
        feed = fetch_feed(url)
        for entry in feed.entries:
            entry['source'] = rss_feed_names[i]
        all_entries.extend(feed.entries)
    # Convert entries to DataFrame
    data = {
        'Title': [entry.title for entry in all_entries],
        'Link': [entry.link for entry in all_entries],
        'Date': [entry.published for entry in all_entries],
        'Summary': [entry.summary for entry in all_entries],
        'Source': [entry.source for entry in all_entries]
    }
    global df
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Sentiment'] = df['Summary'].apply(get_sentiment)
    df['Keywords'] = df['Summary'].apply(extract_keywords)

# Schedule the update_feeds function to run every hour
schedule.every(1).hour.do(update_feeds)  # New scheduling line

# Function to run the scheduler in a separate thread
def run_scheduler():  # New function for running the scheduler
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the scheduler thread
scheduler_thread = threading.Thread(target=run_scheduler)  # New threading line
scheduler_thread.start()  # New threading line

# Default list of RSS feed URLs
default_rss_feeds = {
    'Bleeping Computer': 'https://www.bleepingcomputer.com/feed/',
    'The Hacker News': 'https://thehackernews.com/feeds/posts/default',
    # Add more default RSS feed URLs here
}

# Streamlit app
st.title('Cybersecurity News Dashboard')

# RSS Feed Management
st.sidebar.title('Manage RSS Feeds')
rss_feeds = st.sidebar.text_area('Enter RSS feed URLs (one per line)', '\n'.join(default_rss_feeds.values()))
rss_feeds = rss_feeds.split('\n')
rss_feed_names = [f'Feed {i+1}' for i in range(len(rss_feeds))]

# Initial fetch and combine all feeds
all_entries = []
update_feeds()  # Changed to call the new update_feeds function

# Sentiment Analysis
def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

# Keyword Extraction
def extract_keywords(text):
    words = re.findall(r'\w+', text.lower())
    return [word for word in words if len(word) > 3]

# Trending Topics
all_keywords = [keyword for keywords in df['Keywords'] for keyword in keywords]
trending_topics = Counter(all_keywords).most_common(10)

# Pagination
items_per_page = 10
total_pages = max((len(df) - 1) // items_per_page + 1, 1)
page = st.slider('Page', 1, total_pages, 1)

start_idx = (page - 1) * items_per_page
end_idx = start_idx + items_per_page
paginated_df = df.iloc[start_idx:end_idx]

# Display news articles in a side-by-side block layout
for i in range(0, len(paginated_df), 2):
    cols = st.columns(2)
    for j in range(2):
        if i + j < len(paginated_df):
            with cols[j]:
                row = paginated_df.iloc[i + j]
                st.subheader(row['Title'])
                st.write(row['Summary'])
                st.markdown(f"Read more")
                st.write(f"Published on: {row['Date']}")
                st.write(f"Sentiment: {'Positive' if row['Sentiment'] > 0 else 'Negative' if row['Sentiment'] < 0 else 'Neutral'}")
                st.markdown("---")

# Visualization: Number of articles per source
source_counts = df['Source'].value_counts()
fig, ax = plt.subplots()
source_counts.plot(kind='bar', ax=ax)
ax.set_title('Number of Articles per Source')
ax.set_xlabel('Source')
ax.set_ylabel('Number of Articles')
st.pyplot