import oauth2 as oauth
import os
import troll_data
import twitter
import urlparse

from flask import flash, Flask, jsonify, redirect, request, render_template, session
from model import Account, connect_to_db, db, Tweet
from naive_bayes import classify

app = Flask(__name__)
app.secret_key = "soemonov"

api = None

consumer_key = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']

consumer = oauth.Consumer(consumer_key, consumer_secret)

request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'
authorize_url = 'https://api.twitter.com/oauth/authenticate'


@app.route("/")
def sign_in():
    """Display sign in page."""

    twitter_token = session.get('twitter_token')

    if twitter_token:
        flash("Welcome @{}!".format(session["user"][1]))
        return redirect("/TrolliAm")

    return render_template("sign_in.html")


@app.route("/logout")
def logout():
    flash("See you next time, @{}!".format(session["user"][1]))

    session.clear()

    return redirect("/")


@app.route("/TrolliAm")
def index():
    """Display TrolliAm homepage."""

    twitter_token = session.get('twitter_token')

    if not twitter_token:
        return redirect("/sign_in")

    set_api(twitter_token)

    return render_template("index.html")


def set_api(twitter_token):
    """Maybe should figure out a way to do this without a global variable."""
    global api

    api = twitter.Api(consumer_key, consumer_secret, twitter_token[0],
                      twitter_token[1])


@app.route("/authorize")
def auth():
    twitter_token = session.get('twitter_token')

    if twitter_token:
        flash("Welcome @{}".format(session['user'][1]))
        set_api(twitter_token)

        return redirect("/")

    else:
        client = oauth.Client(consumer)

        resp, content = client.request(request_token_url, "GET")

        if resp['status'] != '200':
            return redirect("/sign_in")

        request_token = dict(urlparse.parse_qsl(content))

        session['request_token'] = (request_token['oauth_token'],
                                    request_token['oauth_token_secret'])

        authorize = "{}?oauth_token={}".format(authorize_url, request_token['oauth_token'])

        return redirect(authorize)


@app.route("/set-access")
def set_access_token():
    oauth_verifier = request.args.get("oauth_verifier")

    if not oauth_verifier:
        session.clear()
        flash("You haven't authorized the TrolliAm app")
        return redirect("/sign_in")

    token = oauth.Token(session['request_token'][0], session['request_token'][1])
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)

    resp, content = client.request(access_token_url, "POST")
    access_token = dict(urlparse.parse_qsl(content))

    session['user'] = (access_token['user_id'], access_token['screen_name'])
    session['twitter_token'] = (access_token['oauth_token'],
                                access_token['oauth_token_secret'])

    set_api(session['twitter_token'])

    return redirect("/")


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


def get_id(tweet_url):
    """
    Retrieves tweet id from url.

    Return values
        _: tweet id
    """
    return tweet_url.split("/")[-1]


@app.route("/tweet-dates.json")
def get_tweet_dates():

    dates = db.session.query(Tweet.created_str).all()

    #get rid of time stamp
    all_dates = [item[0].split()[0] for item in dates if item[0]]
    #get rid of day, only month and year
    only_months = [item.split("-")[:2] for item in all_dates]

    data = troll_data.count_per_month(only_months)

    return jsonify({"data": data})


@app.route("/account-dates.json")
def get_account_data():
    dates = db.session.query(Account.created_at).all()

    data = troll_data.count_per_year(dates)
    #only_months = troll_data.parse_account_data(dates)

    #data = troll_data.count_per_month(only_months)

    return jsonify({"data": data})


@app.route("/common-words.json")

def get_common_words():

    if hasattr(get_common_words, 'response'):
        return get_common_words.response

    all_text = db.session.query(Tweet.text).all()

    most_common = troll_data.get_words(all_text)

    response = jsonify({"data": most_common})
    
    get_common_words.response = response
    
    return response

if __name__ == '__main__':
    connect_to_db(app)
    app.run(port=5000, host='0.0.0.0', debug=True)
