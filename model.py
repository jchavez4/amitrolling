"""Models and database functions for AmIBot project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Tweet(db.Model):
    """Tweets model."""

    __tablename__ = "tweets"

    t_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.BigInteger)
    user_key = db.Column(db.String(64), db.ForeignKey('accounts.screen_name'))
    created_str = db.Column(db.String(64))
    retweet_count = db.Column(db.String(64))
    retweeted = db.Column(db.String(64))
    favorite_count = db.Column(db.String(64))
    text = db.Column(db.String(280))
    tweet_id = db.Column(db.BigInteger)
    source = db.Column(db.String(512))
    hashtags = db.Column(db.String(512))
    mentions = db.Column(db.String(512))

    account = db.relationship("Account", backref=db.backref("tweets"))

    def __repr__(self):
        """Provide helpful representation of a Tweet when printed."""

        return "<Tweet user_id={} tweet_id={}".format(self.user_id,
                                                      self.tweet_id)


class Account(db.Model):
    """Twitter Accounts model."""

    __tablename__ = "accounts"

    user_id = db.Column(db.BigInteger)
    location = db.Column(db.String(64))
    name = db.Column(db.String(64))
    followers_count = db.Column(db.String(64))
    statuses_count = db.Column(db.String(64))
    time_zone = db.Column(db.String(64))
    verified = db.Column(db.String(64))
    lang = db.Column(db.String(2))
    screen_name = db.Column(db.String(64), primary_key=True)
    description = db.Column(db.String(280))
    created_at = db.Column(db.String(64))
    favorites_count = db.Column(db.String(64))
    friends_count = db.Column(db.String(64))
    listed_count = db.Column(db.String(64))

    def __repr__(self):
        """Provide helpful representation of an Account when printed."""

        return "<Account user_id={} screen_name={}".format(self.user_id,
                                                           self.screen_name)


def connect_to_db(app):
    """Connect database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///tweets'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."
