import praw
import config
# Define user agent
user_agent = "praw_scraper_1.0"

# Create an instance of reddit class
reddit = praw.Reddit(username=config.username,
                     password=config.password,
                     client_id=config.client_id,
                     client_secret=config.client_secret,
                     user_agent=user_agent)

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download(["vader_lexicon"])
sia = SentimentIntensityAnalyzer()

runningSum = 0
commentsViewed = 0
maxComments = 500
for submission in reddit.subreddit('fantasyfootball+nfl').new():
    print(submission.title)
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        commentsViewed += 1
        if 'Eagles' in comment.body:
            runningSum += sia.polarity_scores(comment.body)['compound']
            print(runningSum)
        if maxComments < commentsViewed:
            break
    if maxComments < commentsViewed:
            break
    