from nltk.sentiment.vader import SentimentIntensityAnalyzer

se = SentimentIntensityAnalyzer()
se2 = SentimentIntensityAnalyzer(lexicon_file='/home/mihael/Documents/8. semestar/SEMINAR/git/Implementacija/lexicon'
                                              '/L2/filtered/l2_lexicon_formatted.txt')

print(se.polarity_scores("I love being ignored"))
print(se2.polarity_scores("I love being ignored"))

print("-----")
for word in "I love being ignored".split():
    print("SE: " + word + " -> " + str(se.polarity_scores(word)))
    print("SE2: " + word + " -> " + str(se.polarity_scores(word)))