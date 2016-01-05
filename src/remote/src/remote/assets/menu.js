$(document).ready(function() {
    $.getJSON("http://localhost:8898/__about__", function(data) {
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
