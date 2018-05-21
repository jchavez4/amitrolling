"use strict";

function embedTweet(evt) {
    evt.preventDefault();

    let data = {"tweet": $("#tweet-link").val()};

    $.post("/get-embed-tweet.json", data, function(results) {
        $("#embed-tweet").html(results.html);
    });
}

function getLabel(evt) {
    evt.preventDefault();

    $("#label").empty();

    let data = {"tweet": $("#tweet-link").val()};

    $.post("/get-label.json", data, function(results) {
        $("#label").html(results.label);
    });
}

$("#tweet-link").on("input", embedTweet);

$("#tweet-form").on("submit", getLabel);