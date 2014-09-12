$(function () {
	$.getJSON('/api/top_drops?machine_id=' + machine_id, function(json) {
		$('#top_drops_total').highcharts({
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
				text: 'Popularity of Drops for ' + machine_name
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
				name: 'Drops',
				point: {
					events: {
						click: function(e) {
							location.href = e.point.url;
							e.preventDefault();
						}
					}
				},
				data: json, 
			}]
		});
	});
});

$(function() {
	$.getJSON('/api/machine/' + machine_id, function(data) {
		$('#drops_over_time').highcharts('StockChart', {
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
				text : 'Total Items Dropped from ' + machine_name
			},
			yAxis: {
				min: 0
			},
			series : [{
				name : 'Drops ',
				data : data,
			}]
		});
	});
});

$(function () {
	$.getJSON('/api/hours?machine_id=' + machine_id, function(json) {
		$('#drops_over_hours').highcharts({
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
				text: 'Drops by the Hour for ' + machine_name
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
				categories: ['1am', '2am', '3am', '4am', '5am', '6am', '7am',
					'8am', '9am', '10am', '11am', 'noon', '1pm', '2pm', '3pm',
					'4pm', '5pm', '6pm', '7pm', '8pm', '9pm', '10pm', '11pm',
					'midnight']
			},
			yAxis: {
				title: {
					text: '# of Drops'
				}
			},
			tooltip: {
				shared: true,
				valueSuffix: ' drops'
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
				name: 'Drops',
				data: json
			}]
		});
	});
});

