import os
import twitter

from flask import Flask, request, render_template, jsonify
from model import connect_to_db
from naive_bayes import classify

app = Flask(__name__)
app.secret_key = "soemonov"


@app.route("/")
def index():
    """Display homepage."""

    return render_template("index.html")


@app.route("/get-label.json", methods=["POST"])
def get_label():
    """
    Retrieves link from user and runs classifier on tweet.

    Return values
        _: jsonified response containing label of either 'troll' or 'nontroll'
    """

    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    tweet_url = request.form.get("tweet")
    tweet_id = get_id(tweet_url)

    status = api.GetStatus(tweet_id)

    label = classify(status.text)

    return jsonify({"label": label})


def get_id(tweet_url):
    """
    Retrieves tweet id from url.

    Return values
        _: tweet id
    """
    return tweet_url.split("/")[-1]


if __name__ == '__main__':
    connect_to_db(app)
    app.run(port=5000, host='0.0.0.0', debug=True)
