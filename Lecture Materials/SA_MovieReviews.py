import nltk
from nltk.corpus import movie_reviews
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import random, string
stop = stopwords.words('english')

# for i in stop: print i
# print(movie_reviews.raw('pos/cv957_8737.txt'))
# print(movie_reviews.fileids())
      
documents = [(list(movie_reviews.words(fileid)), category)
            for category in movie_reviews.categories()
            for fileid in movie_reviews.fileids(category)]

#print(documents[0])

random.shuffle(documents)

all_words = FreqDist(w.lower() for w in movie_reviews.words()) # Book version
# all_words = FreqDist(w.lower() for w in movie_reviews.words() if w.lower() not in stop and w.lower() not in string.punctuation)

# Limit the number of features that the classifier needs to process to the 2,000 most frequent words
# word_features = all_words.keys()[:2000] # wrong
# word_features = list(all_words)[:2000]  # wrong
word_features = [w for (w, c) in all_words.most_common(2000)]
#print(word_features[:100])

def document_features(document): # a feature extractor, input document is a list of words/tokensis in that document
    # checking whether a word occurs in a set is much faster than checking whether it occurs in a list
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features

#print(document_features(movie_reviews.words('pos/cv957_8737.txt')))

# Training and testing a classifier for document classification.
featuresets = [(document_features(d), c) for (d,c) in documents]
train_set, test_set = featuresets[100:], featuresets[:100]


classifier = nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, test_set))
classifier.show_most_informative_features(30) # defalut 10
print()

"""
# for Decision Trees
classifier = nltk.DecisionTreeClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, test_set))
print(classifier.pretty_format(depth=5))
"""


