"use strict";

function embedTweet(evt) {
    evt.preventDefault();

    let data = {"tweet": $("#tweet-link").val()};

    $.post("/get-embed-tweet.json", data, function(results) {
        $("#embed-tweet").html(results.html);
    });
}

$("#tweet-link").on("input", embedTweet);

function getLabel(evt) {
    evt.preventDefault();

    $("#label").empty();

    let data = {"tweet": $("#tweet-link").val()};

    $.post("/get-label.json", data, function(results) {
        $("#label").html("This has been classified as a " + results.label + " tweet.");
    });
}

$("#tweet-form").on("submit", getLabel);

let tweetResults = [];
let accountResults = [];
let wordCloudResults = [];
let labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
let marker = [
                {
                    drawTime: "afterDatasetsDraw",
                    id: "vline",
                    type: "line",
                    mode: "vertical",
                    scaleID: "x-axis-0",
                    value: "Oct",
                    borderColor: "black",
                    borderWidth: 5,
                    label: {
                      backgroundColor: "#F30261",
                      content: "2016 Presidential Election",
                      enabled: true
                    }
                }
            ];

Chart.defaults.global.defaultFontColor = "white";
Chart.defaults.global.defaultFontSize = 22;
Chart.defaults.global.defaultFontFamily = "'Montserrat', 'sans-serif'";

$.get("/tweet-dates.json", function (results) {
    tweetResults = results.data;
    renderCharts(tweetResults);
});

$.get("/account-dates.json", function (results) {
    accountResults = results.data;
    renderCharts(accountResults);
});

$.get("/common-words.json", function (results) {
    wordCloudResults = results.data;
    renderCharts(wordCloudResults);
});

function renderCharts(results) {
    if (tweetResults.length && accountResults.length && wordCloudResults.length) {
        drawTweetChart(tweetResults);
        drawAccountChart(accountResults);
        drawWordCloud(wordCloudResults);
    }

}

function drawTweetChart(results) {
    let ctx_tweet_line = $("#tweetTimeChart").get(0).getContext("2d");

    new Chart(ctx_tweet_line, {
        type: 'line',
        data: {"labels": labels,
                 "datasets": [
                    {
                        "label": "2016",
                        "fill": false,
                        "data": results[0],
                        "borderColor": "#00E8E7"
                    },

                    {
                        "label": "2017",
                        "fill": false,
                        "data": results[1],
                        "borderColor": "#EDBC05"
                    }
                ]
        },
        options: {
            responsive : true,
            title: {
                display: true,
                text: 'Tweets from Troll Accounts per Month'
            },
            annotation: {
                annotations: marker
            },
        }
    });
}

function drawAccountChart(results) {
    let ctx_account = $("#accountTimeChart").get(0).getContext("2d");

    new Chart(ctx_account, {
        type: 'bar',
        data: {"labels": ["2013", "2014", "2015", "2016"],
                 "datasets": [
                    {
                        "fill": false,
                        "data": results,
                        "backgroundColor": "#F30261",
                        "borderColor": "#F30261",
                        "borderWidth": 1
                    },
                ]
        },
        options: {
            responsive : true,
            legend : {
                display: false
            },
            annotation: {
                annotations: marker
            },
            title: {
                display: true,
                text: 'Number of Troll Accounts Created per Year'
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

function drawWordCloud(results) {
    let word_cloud = $("#wordCloud").get(0);

    WordCloud(word_cloud, {
        list: results,
        weightFactor: 3.5,
        fontFamily: 'Montserrat, sans-serif',
        color: function (word, weight) {
            return (["#F30261", "#250447", "#00E8E7", "#EDBC05"])[Math.floor(Math.random() * 4)];
        },
        hover: function (item) {
            if (item) {
                let percent = parseFloat(item[1]).toFixed(2);
                let message = percent + "% of the words in the dataset of troll tweets is '" + item[0] + "'";
                $("#wordCloud").prop("title", message);
            }
        },
        backgroundColor: '#ffffff',
        rotateRatio: 0
    });
}

$( ".selector" ).autocomplete({
focus: function (event, ui) {
                $(".ui-helper-hidden-accessible").hide();
                event.preventDefault();
            }
});

$(document).ready(function(){
    try {
        $("#wordCloud").tooltip();
    }
    catch (e) {
        console.log(e);
    } 
});