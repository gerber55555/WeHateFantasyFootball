from pathlib import Path

import praw
import config
import pprint
import psaw
import logging
pp = pprint.PrettyPrinter(indent=4)
# Define user agent
user_agent = "praw_scraper_1.0"

# Create an instance of reddit class
reddit = praw.Reddit(username=config.username,
                     password=config.password,
                     client_id=config.client_id,
                     client_secret=config.client_secret,
                     user_agent=user_agent)
api = psaw.PushshiftAPI(reddit)

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from GetPlayerProjectedPoints import get_player_stats
import pandas as pd
import datetime as dt
nltk.download(["vader_lexicon"])
sia = SentimentIntensityAnalyzer()

runningSum = 0
commentsViewed = 0
maxComments = 1000000
players = get_player_stats()
players = players.sort_values('Projected Points', ascending=False)
players = players.head(250)
players = players.set_index('Full Name')

start_epoch=int(dt.datetime(2022, 10, 23).timestamp())
end_epoch=int(dt.datetime(2022, 11, 19).timestamp())

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

logger = logging.getLogger('psaw')
logger.setLevel(logging.INFO)
logger.addHandler(handler)

for name, row in players.iterrows():
    for comment in api.search_comments(q=name, subreddit='fantasyfootball', limit=1000, after=start_epoch, before=end_epoch):
        score = sia.polarity_scores(comment.body)['compound']
        if score < players.loc[name, "Most Negative Comment Score"]:
            players.loc[name, "Most Negative Comment Score"] = score
            players.loc[name, "Most Negative Comment"] = comment.body
        if score > players.loc[name, "Most Positive Comment Score"]:
            players.loc[name, "Most Positive Comment Score"] = score
            players.loc[name, "Most Positive Comment"] = comment.body
        players.loc[name, "Sentiment"] += score
        players.loc[name, "NumOfDataPoints"] += 1


for name, row in players.iterrows():
    if row["NumOfDataPoints"] > 0:
        row["Average Sentiment"] = row["Sentiment"]/row["NumOfDataPoints"]

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(players)

players.to_csv(Path('test.csv'))
