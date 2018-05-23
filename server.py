import os
import twitter
import oauth2 as oauth
import urlparse

from flask import flash, Flask, jsonify, redirect, request, render_template, session
from model import connect_to_db
from naive_bayes import classify

app = Flask(__name__)
app.secret_key = "soemonov"

api = None

consumer_key = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']

consumer = oauth.Consumer(consumer_key, consumer_secret)

request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'
authorize_url = 'https://api.twitter.com/oauth/authorize'


@app.route("/")
def index():
    """Display homepage."""

    return render_template("index.html")


@app.route("/sign_in")
def sign_in():
    """
    """

    return render_template("sign_in.html")


@app.route("/authorize")
def auth():
    client = oauth.Client(consumer)

    resp, content = client.request(request_token_url, "GET")

    if resp['status'] != '200':
        return redirect("/sign_in")

    request_token = dict(urlparse.parse_qsl(content))

    #instead of storing in session, should store in db for security
    session['oauth_token'] = request_token['oauth_token']
    session['oauth_token_secret'] = request_token['oauth_token_secret']

    authorize = "{}?oauth_token={}".format(authorize_url, request_token['oauth_token'])

    return redirect(authorize)


@app.route("/set-access")
def set_accesss_token():
    global api

    oauth_verifier = request.args.get("oauth_verifier")

    if not oauth_verifier:
        session.clear()
        flash("You haven't authorized the TrolliAm app")
        return redirect("/sign_in")

    token = oauth.Token(session['oauth_token'], session['oauth_token_secret'])
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)

    resp, content = client.request(access_token_url, "POST")
    access_token = dict(urlparse.parse_qsl(content))

    #access_token has user_id, should save user_id, token, token_secret in db
    #so user doesn't have to authorize app every time.

    #can save user_id in a session so that it doesn't redirect them to
    #re-authorize, need to add logout button then to clear session

    #how to check if user is signed in to twitter or not?

    #setting api to use user's keys
    api = twitter.Api(consumer_key, consumer_secret,
                      access_token['oauth_token'],
                      access_token['oauth_token_secret'])

    return redirect("/")


@app.route("/get-label.json", methods=["POST"])
def get_label():
    """
    Retrieves link from user and runs classifier on tweet.

    Return values
        _: jsonified response containing label of either 'troll' or 'nontroll'
    """

    tweet_url = request.form.get("tweet")
    tweet_id = get_id(tweet_url)

    status = api.GetStatus(tweet_id)

    label = classify(status.text)

    return jsonify({"label": label})


@app.route("/get-embed-tweet.json", methods=["POST"])
def embed_tweet():
    """
    Retrieves link from input and returns embeddable form.

    Return values
        _: jsonified response containing information for embeddable tweet
    """

    tweet_url = request.form.get("tweet")

    status = api.GetStatusOembed(url=tweet_url)

    return jsonify(status)


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
