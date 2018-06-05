import calendar
import nltk
import string
import re

from collections import Counter
from nltk.corpus import stopwords

#stopwords = nltk.download("stopwords")
#nltk.download('words')

#could do timeline of tweets
#do timeline of creation of accounts
#most frequent words found in the russian troll tweets in general
    #most frequent words before election
    #most frequent words after election


def parse_account_data(dates):
    only_months = []

    for date in dates:
        tmp = []
        if date[0]:
            separated = date[0].split()
            tmp.append(separated[-1])
            #get numerical month from str abbreviation
            month = list(calendar.month_abbr).index(separated[1])
            tmp.append(month)
            only_months.append(tmp)

    return only_months


def count_per_month(only_months):
    years = {}

    #create double dictionary to get counts per year per month of tweets
    for date in only_months:
        years[int(date[0])] = years.get(int(date[0]), {})

        month_dict = years.get(int(date[0]))

        month_dict[int(date[1])] = month_dict.get(int(date[1]), 0) + 1

    #create list of counts per month per year to send
    month_counts = []
    for key, value in sorted(years.items()):
        if key == 2016 or key == 2017:
            counts = []
            for month, count in sorted(years.get(key).items()):
                counts.append(count)
            month_counts.append(counts)

    return month_counts

def get_words(all_text):
    only_words = []

    regex = re.compile('[^a-zA-Z]')
    stop = set(stopwords.words("english") + ["rt", "via", "https", "amp"])

    for item in all_text:
        if item[0]:
            no_punct = item[0].encode("utf-8").translate(None, string.punctuation)
            words = no_punct.strip(".").split()
        for word in words:
            word = regex.sub('', word).lower()
            if word not in stop and "http" not in word and not word.isdigit():
                only_words.append(word)

    c = Counter(only_words)

    top_100 = normalize_count(c)

    return top_100

def normalize_count(c):
    #total number of valid words in corpus of text
    key_max = max(c.keys(), key=(lambda k: c[k]))
    key_min = min(c.keys(), key=(lambda k: c[k]))

    old_max = c[key_max] + 10000
    old_min = 10

    total_count = len(list(c.elements()))
    top_100 = []

    for item in c.most_common(100):
        old = (item[1] - old_min)/float(old_max - old_min)
        new = ((50 - 10) * old) + 10

        top_100.append([item[0], new])

    return top_100
