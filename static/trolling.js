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

let ctx_line = $("#tweetTimeChart").get(0).getContext("2d");

$.get("/tweet-dates.json", function (results) {
    //console.log(results.datasets.months);
    let myLineChart = new Chart(ctx_line, {
        type: 'line',
        data: results,
        options: {
            responsive : true,
            scales: {
                xAxes: [{
                    time: {
                        unit: 'month'
                    }
                }]
            }
        }
    });

    $("#tweetLegend").html(myLineChart.generateLegend());
});