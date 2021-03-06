$(function() {
	var cache = {};
	$('#query').autocomplete({
		minLength: 2,
		source: function(request, response) {
			var term = request.term;
			if (term in cache) {
				response(cache[term]);
				return;
			}
			$.getJSON("/autocomplete", request, function(data, status, xhr) {
				cache[term] = data;
				response(data);
			});
		}
	});
});
	
