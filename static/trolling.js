"use strict";

function getLabel(evt) {
    evt.preventDefault();

    let data = {"tweet": $("#tweet-link").val()};

    $.post("/get-label.json", data, function(results) {
        console.log(results["html"]);
        $("#embed-tweet").html(results["html"]);
        $("#label").html(results["label"]);
    });
}

$("#tweet-form").on("submit", getLabel);
