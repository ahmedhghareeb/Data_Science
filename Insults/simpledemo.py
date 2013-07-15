#import regex
import re
import csv
import pprint
import nltk.classify
import pdb

#start replaceTwoOrMore
def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)
#end

#start process_tweet
def processTweet(tweet):
    # process the tweets

    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet
#end

#start getfeatureVector
def getFeatureVector(tweet):
    featureVector = []
    words = tweet.split()
    for w in words:
        #replace two or more with two occurrences
        w = replaceTwoOrMore(w)
        #strip punctuation
        w = w.strip('\'"?,.')
        #check if it consists of only words
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*$", w)
        featureVector.append(w.lower())
    return featureVector
#end

#start get_bad_word_list
def get_bad_word_list(fileName):
    fp = open(fileName, 'r')
    line = fp.readline()
    featureList = []
    while line:
        line = line.strip()
        featureList.append(line)
        line = fp.readline()
    fp.close()
    return featureList
#end

#start extract_features
def extract_features(tweet):
    # pdb.set_trace()
    tweet_words = set(tweet)
    features = {}
    for word in featureList:
        features['contains(%s)' % word] = (word in tweet_words)
    return features
#end


#Read the tweets one by one and process it
comments = csv.reader(open('train.csv', 'rb'), delimiter=',')
featureList = get_bad_word_list('badwords.txt')
count = 0;
tweets = []
for row in comments:
    insult = row[0]
    tweet = row[2]
    processedTweet = processTweet(tweet)
    featureVector = getFeatureVector(processedTweet)
    # pdb.set_trace()
    tweets.append((featureVector, insult));
#end loop

training_set = nltk.classify.util.apply_features(extract_features, tweets)
#pp.pprint(training_set)

# Train the Naive Bayes classifier
NBClassifier = nltk.NaiveBayesClassifier.train(training_set)

# Test the classifier
testTweet = 'You fuck your dad'
processedTestTweet = processTweet(testTweet)
insult = NBClassifier.classify(extract_features(getFeatureVector(processedTestTweet)))
print "testTweet = %s, insult = %s\n" % (testTweet, insult)
