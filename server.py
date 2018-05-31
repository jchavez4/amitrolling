import oauth2 as oauth
import os
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


@app.route("/get-timeline.json")
def embed_timeline():
    tweets = api.GetHomeTimeline()

    timeline_id = create_collection(tweets)

    html = '<a class="twitter-timeline"href="https://twitter.com/{}/timelines/{}">{}</a>'.format("_", timeline_id, "User Timeline")

    return jsonify({"html": html})


def create_collection(tweets):
    payload = {'name': 'test_collection'}
    response = api._RequestUrl('https://api.twitter.com/1.1/collections/create.json',
                               'POST', data=payload)

    data = api._ParseAndCheckTwitter(response.content.decode('utf-8'))

    timeline_id = data['response']['timeline_id']

    for tweet in tweets:
        payload = {'id': timeline_id, 'tweet_id': tweet.id}
        response = api._RequestUrl('https://api.twitter.com/1.1/collections/entries/add.json',
                                   'POST', data=payload)

    return timeline_id


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
    month_counts = []
 
    dates = db.session.query(Tweet.created_str).all()
    #get rid of time stamp
    all_dates = [item[0].split()[0] for item in dates if item[0]]
    #get rid of day, only month and year
    only_months = [item.split("-")[:2] for item in all_dates]

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

    data_dict = {
            "labels": [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec"
            ],
            "datasets": [
                {
                    "data": month_counts[0],
                    "backgroundColor": [
                        "#FF6384",
                        "#36A2EB",
                    ],
                    "hoverBackgroundColor": [
                        "#FF6384",
                        "#36A2EB",
                    ]
                }]
        }

    return jsonify(data_dict)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(port=5000, host='0.0.0.0', debug=True)
