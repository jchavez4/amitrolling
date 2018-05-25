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
    console.log("timeline will load now.");
}

$(window).on("load", embedTimeline);

function getLabel(evt) {
    evt.preventDefault();

    $("#label").empty();

    let data = {"tweet": $("#tweet-link").val()};

    $.post("/get-label.json", data, function(results) {
        $("#label").html(results.label);
    });
}

$("#tweet-form").on("submit", getLabel);