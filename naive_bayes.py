import numpy as np
import pandas as pd
import pickle

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn import cross_validation
from sklearn import metrics


def load_data():
    """
    Load and organize tweets for classification.

    Return values
        text: list of text from tweets
        labels: list of corresponding target labels

    """

    #read in troll tweets
    nt_df = pd.read_csv('nontroll-tweets/non_troll.csv', names=['target', 'tweet_id',
                                                                'date', 'flag',
                                                                'user_key', 'text'])

    #randomly select tweets from nontroll dataset to approx. match troll dataset size
    nt_df = nt_df.sample(n=203482)

    #read in nontroll tweets
    t_df = pd.read_csv('troll-tweets/tweets.csv')

    #remove entries with an empty text field from troll dataset
    t_df = t_df.dropna(subset=['text'])

    troll_tweets = []
    nontroll_tweets = []

    #create lists of labeled tweets
    for index, row in t_df.iterrows():
        troll_tweets.append((row['text'], 'troll'))

    for index, row in nt_df.iterrows():
        nontroll_tweets.append((row['text'], 'nontroll'))

    #create masterlist of labeled tweets
    tweets = troll_tweets + nontroll_tweets

    #unzip masterlist of tweets
    text, labels = [list(item) for item in zip(*tweets)]

    return text, labels


def freq_matrix():
    """
    Creates a frequency matrix for tweet dataset.

    Return values
        X: term frequency matrix
        y: numpy array of target labels
    """

    text, labels = load_data()

    #ignore 'dirty' data, text not UTF8 when creating vectorizer
    vectorizer = TfidfVectorizer(decode_error='ignore')

    #returns matrix
    X = vectorizer.fit_transform(text)
    y = np.array(labels)

    with open('vectorizer.pickle', 'wb') as v:
        pickle.dump(vectorizer, v)

    return X, y


def train(X, y):
    """
    Train and evaluate Bernoulli Naive Bayes classifier.

    Return values
        _: Trained Bernoulli Naive Bayes classifier pickled as a string
    """

    clf = BernoulliNB()

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y,
                                                                         test_size=0.65)

    clf.fit(X_train, y_train)

    #add prediction evaluation
    #y_predictions = clf.predict(X_test, y_test)

    with open('classifier.pickle', 'wb') as c:
        pickle.dump(clf, c)


def classify(tweet_text):
    """
    Classify given tweet as either 'troll' or 'nontroll'.

    Return values
        label: String containing either 'troll' or 'nontroll'

    """

    with open('vectorizer.pickle') as v:
        vectorizer = pickle.load(v)

    with open('classifier.pickle') as c:
        clf = pickle.load(c)

    tweet_matrix = vectorizer.transform([tweet_text])

    label = clf.predict(tweet_matrix)

    return label[0]

if __name__ == '__main__':
    X, y = freq_matrix()

    train(X, y)

    test_label = classify("yo yo yo am i a troll.")

    print test_label
