$(document).ready(function() {

    $.getJSON("http://karl.novareto.de:7080/__about__", function(data) {
	var items = [];
	$.each(data, function(key, val) {
	    items.push( "<li><a href='" + key + "'>" + val + "</a></li>");
	});
	$( "<ul/>", {
	    "id": "remotewsgi",
	    html: items.join("")
	}).appendTo("body");
    }); 
});
