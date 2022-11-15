import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download(["vader_lexicon"])
sia = SentimentIntensityAnalyzer()
sia.polarity_scores("This is a great test phrase!")
