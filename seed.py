"""Functions used to seed database with troll data"""
import pandas as pd
import numpy as np
from model import Tweet, Account, connect_to_db, db
from server import app


def load_accounts(data='troll-tweets/users.csv'):
    """Load user accounts from users.csv into database."""

    df = pd.read_csv(data)

    df['id'].replace(np.nan, 0, regex=True, inplace=True)
    df.replace(np.nan, '', regex=True, inplace=True)

    for index, row in df.iterrows():
        user_id, location, name, followers_count, statuses_count, time_zone,\
        verified, lang, screen_name, description, created_at, favorites_count,\
        friends_count, listed_count = row.values.tolist()

        if user_id == '':
            account = Account(screen_name=screen_name)
        else:
            account = Account(user_id=user_id, location=location, name=name,
                              followers_count=followers_count, statuses_count=statuses_count,
                              time_zone=time_zone, verified=verified, lang=lang,
                              screen_name=screen_name.lower(), description=description,
                              created_at=created_at, favorites_count=favorites_count,
                              friends_count=friends_count, listed_count=listed_count)

        db.session.add(account)

    db.session.commit()


def load_tweets(data='troll-tweets/tweets.csv'):
    """Load tweets from tweets.csv into database."""

    df = pd.read_csv(data)

    df['user_id'].replace(np.nan, 0, regex=True, inplace=True)
    df['tweet_id'].replace(np.nan, 0, regex=True, inplace=True)
    df.replace(np.nan, '', regex=True, inplace=True)

    #getting rid of columns not in Tweet model.
    df.drop('created_at', axis=1, inplace=True)
    df.drop('expanded_urls', axis=1, inplace=True)
    df.drop('posted', axis=1, inplace=True)
    df.drop('retweeted_status_id', axis=1, inplace=True)
    df.drop('in_reply_to_status_id', axis=1, inplace=True)

    for index, row in df.iterrows():
        user_id, user_key, created_str, retweet_count,\
        retweeted, favorite_count, text, tweet_id, source,\
        hashtags, mentions = row.values.tolist()

        tweet = Tweet(user_id=user_id, user_key=user_key, created_str=created_str,
                  retweet_count=retweet_count, retweeted=retweeted,
                  favorite_count=favorite_count, text=text, tweet_id=tweet_id,
                  source=source, hashtags=hashtags, mentions=mentions)
        db.session.add(tweet)

    db.session.commit()

if __name__ == '__main__':
    connect_to_db(app)

    db.create_all()

    Tweet.query.delete()
    Account.query.delete()

    load_accounts()
    load_tweets()
