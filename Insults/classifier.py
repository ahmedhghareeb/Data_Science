#########################
# Detecting Insults in Social Commentary
#########################

# Manipulate csvs
import csv
# Regular Expressions
import re
# Python Debugger
import pdb

#########################
# Import NLTK to do Natural Language Processing
# Import the NLTK Classifiers
#########################
import nltk
from nltk.collocations import *
from nltk.classify.svm import SvmClassifier
from nltk.classify.naivebayes import NaiveBayesClassifier

#########################
# Import libraries to analyze bigrams
#########################
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk import bigrams
bigram_measures = nltk.collocations.BigramAssocMeasures()

#########################
# Import libraries to analyze trigrams
#########################
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import TrigramAssocMeasures
from nltk import trigrams
trigram_measures = nltk.collocations.TrigramAssocMeasures()


#########################
# Reads in a txt file and creates a list from the word list
#########################
def get_word_list(wordListFileName):
    word_list = []
    fp = open(wordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        word_list.append(word)
        line = fp.readline()
    fp.close()
    return word_list

#########################
# Takes a tweet string as input and:
# Formats it, Fixes common mispellings, Removes common contractions
#########################
def process_tweet(tweet):
    # Convert to lower case
    tweet = tweet.lower()

    # Fix spellings
    tweet = re.sub("azz", "ass", tweet)
    tweet = re.sub(" u ", " you ", tweet)
    tweet = re.sub(" em ", " them ", tweet)
    tweet = re.sub(" da ", " the ", tweet)
    tweet = re.sub(" yo ", " you ", tweet)
    tweet = re.sub(" ur ", " you ", tweet)

    # Fix contractions
    tweet = re.sub("won't", "will not", tweet)
    tweet = re.sub("wasn't", "was not", tweet)
    tweet = re.sub("can't", "cannot", tweet)
    tweet = re.sub("i'm", "i am", tweet)
    tweet = re.sub(" im ", " i am ", tweet)
    tweet = re.sub("ain't", "is not", tweet)
    tweet = re.sub("'ll", " will", tweet)
    tweet = re.sub("'t", " not", tweet)
    tweet = re.sub("'ve", " have", tweet)
    tweet = re.sub("'s", " is", tweet)
    tweet = re.sub("'re", " are", tweet)
    tweet = re.sub("'d", " would", tweet)

    # Remove URL strings like www.* or https?://*
    tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))', '', tweet)
    # Remove @username
    tweet = re.sub('@[^\s]+', '', tweet)
    # Replace hashtagged words with just the word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)

    # Remove newline characters
    tweet = re.sub('\\\\n', ' ', tweet)
    # Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    # Strip punctuation
    tweet = tweet.strip('\'"?,.')
    # Strip all non-alphabet characters
    tweet = re.sub('[^a-z\']+', ' ', tweet)
    # Strip leading and trailing whitespace
    tweet = tweet.strip()

    return tweet

#########################
# Takes a tweet as input and returns the feature set
#########################
def get_features_from_tweet(tweet):
    # Tokenize the tweet into a list of words
    tokens = process_tweet(tweet).split()

#########################
# Every word in the tweet is added as a feature
#########################
    unigram_features = dict((w, True) for w in tokens)

#########################
# Only words that appear in the unigram_list are added as features
#########################
#    unigram_features = dict()
#    for ug in tokens:
#        if ug in unigram_list:
#            unigram_features[ug] = True

#########################
# The top 10 bigrams as determined by chi squared are added as features
#########################
#    bigram_finder = BigramCollocationFinder.from_words(tokens)
#    tweet_bigrams = bigram_finder.nbest(BigramAssocMeasures.chi_sq, 10)
#    bigram_features = dict((w, True) for w in tweet_bigrams)

#########################
# Only bigrams that appear in the bigram_list are added as features
#########################
#    tweet_bigrams = bigrams(tokens)
#    bigram_features = dict()
#    for bg in tweet_bigrams:
#        if bg in bigram_list:
#            bigram_features[bg] = True

#########################
# The top 10 trigrams as determined by chi squared are added as features
#########################
#    trigram_finder = TrigramCollocationFinder.from_words(tokens)
#    tweet_trigrams = trigram_finder.nbest(TrigramAssocMeasures.chi_sq, 10)
#    trigram_features = dict((w, True) for w in tweet_trigrams)

#########################
# If greater than 60% of the characters in the tweet are upper case, "CAPITALIZED" is added as a feature
#########################
#    cap_feature = dict()
#    cap_percent = float(sum(1 for c in tweet if c.isupper())) / len(tweet)
#    if cap_percent > 0.6:
#        cap_feature = {'CAPITALIZED': True}

#########################
# Return the feature set(s) to be used
#########################
    return dict(unigram_features.items())
#    return dict(unigram_features.items() + bigram_features.items())
#    return cap_feature


#########################
# Compiles the training features from a list of tweets and how they were classified
#########################
def get_train_features_from_tweets(tweets, insult_clean):
    tweet_features = []
    for tweet in tweets:
        features = get_features_from_tweet(tweet)
        tweet_features.append((features, insult_clean))
    return tweet_features

#########################
# Load in a few word lists
# The English stopword list, which turned out not to be effective
# The list of the 100 most useful unigrams
# The list of the 15 most useful bigrams
#########################
stop_words = get_word_list('stopwords.txt')
unigram_list = get_word_list('top.txt')
bigram_list = [('are', 'an'), ('a', 'moron'), ('fuck', 'off'), ('really', 'are'), ('a', 'fool'), ('human', 'being'), ('crawl', 'back'), ('a', 'dumb'), ('fat', 'ass'), ('are', 'a'), ('an', 'idiot'), ('go', 'away'), ('a', 'troll'), ('fuck', 'up'), ('back', 'under')]

#########################
# Load the data in and
# Sort the tweets that were labelled as insults and  "clean" (non-insults)
#########################
insult_tweets = []
clean_tweets = []
train_tweets = csv.reader(open('train.csv', 'rb'), delimiter=',')
for row in train_tweets:
    insult = row[0]
    # the datetime information of the tweet was included, but I ignored it
    tweet = row[2]
    if insult == "1":
        insult_tweets.append(tweet)
    else:
        clean_tweets.append(tweet)

#########################
# Split the data into training and test data
#########################
negcutoff, poscutoff = len(clean_tweets) * 3 / 4, len(insult_tweets) * 3 / 4
clean_train, clean_test = insult_tweets[:poscutoff], insult_tweets[poscutoff:]
insult_train, insult_test = clean_tweets[:negcutoff], clean_tweets[negcutoff:]

insult_feats_train = get_train_features_from_tweets(insult_train, 'insult')
clean_feats_train = get_train_features_from_tweets(clean_train, 'clean')

train_feats = insult_feats_train + clean_feats_train

#########################
# Classifier
# I tried the SVM and Naive Bayes classifiers that come with NLTK
# Since Naive Bayes retains the original feature set, I found it worked well here
# Naive Bayes also performed better in the evaluation
#########################
classifier = NaiveBayesClassifier.train(train_feats)
#classifier = SvmClassifier.train(train_feats)

#########################
# Evaluation
# Use the classifier on the test data and see how it did
#########################
correct, wrong = 0, 0

for tweet in insult_test:
    features = get_features_from_tweet(tweet)
    result = classifier.classify(features)
    if result == "insult":
        correct += 1
    else:
        wrong += 1


for tweet in clean_test:
    features = get_features_from_tweet(tweet)
    result = classifier.classify(features)
    if result == "clean":
        correct += 1
    else:
        wrong += 1


# Print out what the accuracy was in terms of number correct over number attempted
print "Accuracy: {}".format(correct / float(correct + wrong))

# Show the 10 most informative features (I looked at a lot more when I was tinkering)
classifier.show_most_informative_features(10)
