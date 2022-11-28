from pathlib import Path
import praw
import config
import psaw
import logging
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
from GetPlayerProjectedPoints import get_players_stats
import sys
from datetime import datetime, timedelta


# Setup sentiment analysis
def setup_sentiment_analysis_model():
    nltk.download(["vader_lexicon", "punkt"])
    sia = SentimentIntensityAnalyzer()
    return sia


# Setup reddit crawler
def setup_psaw():
    user_agent = "praw_scraper_1.0"
    reddit = praw.Reddit(username=config.username,
                         password=config.password,
                         client_id=config.client_id,
                         client_secret=config.client_secret,
                         user_agent=user_agent)
    api = psaw.PushshiftAPI(reddit)
    __setup_logging_for_psaw()
    return api


def __setup_logging_for_psaw():
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)

    logger = logging.getLogger('psaw')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)


# Get top `number_of_players` by projected points
def get_top_players(number_of_players, week):
    players = get_players_stats(week)
    players = players.sort_values('Projected Points', ascending=False)
    players = players.head(number_of_players)
    players = players.set_index('Full Name')
    return players


week_1_sunday = datetime(2022, 9, 4)
week_1_saturday = datetime(2022, 9, 10)


def get_sentiment_for_top_players(number_of_players, week, file_name=None):
    if file_name is None:
        file_name = f"{week}.csv"
    sia = setup_sentiment_analysis_model()
    api = setup_psaw()
    players = get_top_players(number_of_players, week)
    print(players)

    delta = timedelta(weeks=week - 1)
    start_epoch = int((week_1_sunday + delta).timestamp())
    end_epoch = int((week_1_saturday + delta).timestamp())

    for name, row in players.iterrows():
        for comment in api.search_comments(q=name, subreddit='nfl', limit=1000, after=start_epoch, before=end_epoch):
            for paragraph in comment.body.split('\n'):
                if name.lower() in paragraph.lower():
                    for sentence in sent_tokenize(paragraph):
                        if name.lower() in sentence.lower():
                            score = sia.polarity_scores(sentence)['compound']
                            if score < players.loc[name, "Most Negative Comment Score"]:
                                players.loc[name, "Most Negative Comment Score"] = score
                                players.loc[name, "Most Negative Comment"] = sentence
                            if score > players.loc[name, "Most Positive Comment Score"]:
                                players.loc[name, "Most Positive Comment Score"] = score
                                players.loc[name, "Most Positive Comment"] = sentence
                            players.loc[name, "Sentiment"] += score
                            players.loc[name, "NumOfDataPoints"] += 1

    for name, row in players.iterrows():
        if row["NumOfDataPoints"] > 0:
            row["Average Sentiment"] = row["Sentiment"]/row["NumOfDataPoints"]


    players.to_csv(Path(file_name))


if __name__ == '__main__':
    number_of_players = 10
    week = 1
    file_name = None
    if len(sys.argv) >= 2:
        number_of_players = int(sys.argv[1])
    if len(sys.argv) >= 3:
        week = int(sys.argv[2])
    if len(sys.argv) == 4:
        file_name = sys.argv[3]
    if len(sys.argv) > 4:
        print(f"Expected maximum of 3 arguments but got {sys.argv}")
        exit(-1)

    print(f"Fetching sentiment with parameters: {number_of_players=}, {week=}, {file_name=}")
    get_sentiment_for_top_players(number_of_players, week, file_name)
