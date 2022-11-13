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

for submission in reddit.subreddit('fantasyfootball+nfl').new():
    print(submission.title)
    for comment in submission.comments:
        print(comment.body)