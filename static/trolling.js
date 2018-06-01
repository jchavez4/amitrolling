"use strict";

function embedTweet(evt) {
    evt.preventDefault();

    let data = {"tweet": $("#tweet-link").val()};

    $.post("/get-embed-tweet.json", data, function(results) {
        $("#embed-tweet").html(results.html);
    });
}

$("#tweet-link").on("input", embedTweet);


function embedTimeline(evt) {
    $.get("/get-timeline.json", function(results) {
        $("#embed-timeline").html(results.hmtl);
        console.log(results);
    });
}

//$(window).on("load", embedTimeline);

function getLabel(evt) {
    evt.preventDefault();

    $("#label").empty();

    let data = {"tweet": $("#tweet-link").val()};

    $.post("/get-label.json", data, function(results) {
        $("#label").html(results.label);
    });
}

$("#tweet-form").on("submit", getLabel);

let labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

let ctx_tweet_line = $("#tweetTimeChart").get(0).getContext("2d");

//worry about adding marker later
$.get("/tweet-dates.json", function (results) {
    console.log(results.data[0]);
    console.log(results.data[1]);
    new Chart(ctx_tweet_line, {
        type: 'line',
        data: {"labels": labels,
                 "datasets": [
                    {
                        "label": "2016",
                        "fill": false,
                        "data": results.data[0],
                        "borderColor": "#428ff4"
                    },

                    {
                        "label": "2017",
                        "fill": false,
                        "data": results.data[1],
                        "borderColor": "#7626b7"
                    }
                ]
        },
        options: {
            responsive : true,
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: "Number of Tweets"
                    }
                }]
            }
        }
    });
});

let ctx_account_line = $("#accountTimeChart").get(0).getContext("2d");

$.get("/account-dates.json", function (results) {
    let myLineChart = new Chart(ctx_account_line, {
        type: 'line',
        data: {"labels": labels,
                 "datasets": [
                    {
                        "label": "2016",
                        "fill": false,
                        "data": results.data[0],
                        "borderColor": "#428ff4"
                    }
                ]
        },
        options: {
            responsive : true,
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: "Number of Accounts Created"
                    }
                }]
            }
        }
    });
});