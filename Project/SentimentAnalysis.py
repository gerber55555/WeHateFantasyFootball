import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download(["vader_lexicon"])
sia = SentimentIntensityAnalyzer()

print(sub_toks)

score = sia.polarity_scores("Delusional reddit haters will see just how bad this Cardinals offence is without Kyler Murray.")
print(score)
score = sia.polarity_scores("They can't run for shit so I won't knock them for throwing it a lot (especially since one was a long OT game) but how the fuck do you let Justin Herbert throw it damn near 60 times and end up with such low yardage total")
print(score)
#score = sia.polarity_scores("Josh Allen sucks, Patrick Mahomes is great!")
#print(score['compound'])
#score = sia.polarity_scores("Patrick Mahomes sucks")
#print(score['compound'])
