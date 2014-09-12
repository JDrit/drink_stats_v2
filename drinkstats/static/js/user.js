$(function () {
	$.getJSON('/api/top_drops?username=' + username, function(json) {
		$('#top_drinks_total').highcharts({
			exporting: {
				enabled: false
			},
			credits: {
				enabled: false
			},
			chart: {
				plotBackgroundColor: null,
				plotBorderWidth: null,
				plotShadow: false
			},
			title: {
				text: 'Popularity of Drinks'
			},
			tooltip: {
				pointFormat: '<b>{point.y} {point.name}s</b>'
			},
			plotOptions: {
				pie: {
					allowPointSelect: true,
					cursor: 'pointer',
					dataLabels: {
						enabled: true,
						color: '#000000',
						connectorColor: '#000000',
						format: '<b>{point.name}</b>: {point.percentage:.1f} %'
					}
				}
			},
			series: [{
				type: 'pie',
				name: 'Drinks',
				point: {
					events: {
						click: function(e) {
							location.href = e.point.url;
							e.preventDefault();
						}
					}
				}, 
				data: json
			}]
		});
	});
});

$(function() {
	$.getJSON('/api/user/' + username, function(data) {
		$('#drinks_over_time').highcharts('StockChart', {
			exporting: {
					enabled: false
			},
			credits: {
					enabled: false
			},
			chart: {
					type: 'areaspline'
			},
			rangeSelector : {
					selected : 1
			},
			title : {
					text : 'Total Drinks Dropped for ' + username
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
																																			
$(function () {
	$.getJSON('/api/hours?username=' + username, function(json) {
	$('#drinks_over_hours').highcharts({
			exporting: {
					enabled: false
			},
			credits: {
					enabled: false
			},
			chart: {
					type: 'areaspline'
			},
			title: {
					text: 'Drinks Bought by Hour'
			},
			legend: {
					layout: 'vertical',
					align: 'left',
					verticalAlign: 'top',
					x: 150,
					y: 100,
					floating: true,
					borderWidth: 1,
					backgroundColor: '#FFFFFF'
			},
			xAxis: {
					categories: ['1am', '2am', '3am', '4am', '5am', '6am', '7am', '8am',
						'9am', '10am', '11am', 'noon', '1pm', '2pm', '3pm', '4pm', '5pm',
						'6pm', '7pm',	'8pm', '9pm', '10pm', '11pm', 'midnight']
			},
			yAxis: {
					title: {
							text: '# of Drinks'
					}
			},
			tooltip: {
					shared: true,
					valueSuffix: ' drinks'
			},
			credits: {
					enabled: false
			},
			plotOptions: {
					areaspline: {
							fillOpacity: 0.5
					}
			},
			series: [{
					name: 'Drinks Dropped by ' + username,
					data: json
			}]
		});
	});
});
