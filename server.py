import os

from flask import Flask
from model import connect_to_db

app = Flask(__name__)
app.secret_key = "soemonov"

@app.route("/")
def homepage():
    #add text box for user to enter link
    #call Twitter api to fetch tweet
    #run classifier


if __name__ == '__main__':
    connect_to_db(app)
    app.run(port=5000, host='0.0.0.0')
