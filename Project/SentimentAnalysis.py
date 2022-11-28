import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download(["vader_lexicon"])
sia = SentimentIntensityAnalyzer()

# print(sub_toks)

score = sia.polarity_scores("Josh Allen is GREAT")
print(score)
score = sia.polarity_scores("Josh Allen is great")
print(score)
#score = sia.polarity_scores("Josh Allen sucks, Patrick Mahomes is great!")
#print(score['compound'])
#score = sia.polarity_scores("Patrick Mahomes sucks")
#print(score['compound'])
