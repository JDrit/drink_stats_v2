$(function() {
	$.getJSON('/api/item/' + item_id, function(data) {
		$('#drinks_over_time').highcharts('StockChart', {
			exporting: {
				enabled: false
			},
			credits: {
				enabled: false
			},
			rangeSelector : {
				selected : 1
			},
			chart: {
				type: 'areaspline'
			},
			title : {
				text : item_name + "s Dropped"
			},
			yAxis: {
				min: 0
			},
			series : [{
				name : 'Drinks ',
				data : data,
			}]
		});
	});
});

