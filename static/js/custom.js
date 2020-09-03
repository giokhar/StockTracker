const API_BASE = `${window.location.origin}/api`;

const countify = (selector) => {
	let options = {
		useEasing: true,
		useGrouping: true,
		separator: ',',
		decimal: '.',
		prefix: '',
		suffix: ''
	};
	let countUpElement = document.querySelector(selector);
	let countUp = new CountUp(countUpElement.id, 0, countUpElement.getAttribute('data-count'), 0, 1.5, options);
	countUp.start();
};

window.addEventListener('DOMContentLoaded', () => {

	countify("#investment");


	var thisYearCTX = document.getElementById("thisYearRevenue").getContext("2d");
	var lastYearCTX = document.getElementById("lastYearRevenue").getContext("2d");

	var thisYearData = {
		labels: ["January", "February", "March", "April", "May", "June"],
		datasets: [{
			label: "This year dataset",
			fillColor: "#9C2E9D",
			strokeColor: "#9C2E9D",
			pointColor: "transparent",
			pointStrokeColor: "transparent",
			pointHighlightFill: "#fff",
			pointHighlightStroke: "#9C2E9D",
			data: [45, 62, 15, 78, 58, 98]
		}]
	};

	var lastYearData = {
		labels: ["January", "February", "March", "April", "May", "June"],
		datasets: [{
			label: "Last year dataset",
			fillColor: "#E4E4E4",
			strokeColor: "#E4E4E4",
			pointColor: "transparent",
			pointStrokeColor: "transparent",
			pointHighlightFill: "#fff",
			pointHighlightStroke: "#E4E4E4",
			data: [12, 6, 35, 58, 38, 68]
		}]
	};

	Chart.types.Line.extend({
		name: "LineAlt",
		initialize: function () {
			Chart.types.Line.prototype.initialize.apply(this, arguments);

			var ctx = this.chart.ctx;
			var originalStroke = ctx.stroke;
			ctx.stroke = function () {
				ctx.save();
				ctx.shadowColor = 'rgba(156, 46, 157,0.5)';
				ctx.shadowBlur = 20;
				ctx.shadowOffsetX = 2;
				ctx.shadowOffsetY = 20;
				originalStroke.apply(this, arguments)
				ctx.restore();
			}
		}
	});

	Chart.types.Line.extend({
		name: "LineAlt2",
		initialize: function () {
			Chart.types.Line.prototype.initialize.apply(this, arguments);
			var ctx = this.chart.ctx;
			var originalStroke = ctx.stroke;
			ctx.stroke = function () {
				ctx.save();
				originalStroke.apply(this, arguments)
				ctx.restore();
			}
		}
	});

	var thisYearChart = new Chart(thisYearCTX).LineAlt(thisYearData, {
		datasetFill: false,
		scaleShowGridLines: false,

		datasetStrokeWidth: 5,
		scaleFontColor: '#9e9e9e',
		scaleGridLineColor: '#e4e4e4',
		scaleLineColor: 'transparent',
		scaleOverride: true,
		scaleSteps: 5,
		scaleStepWidth: 20,
		scaleStartValue: 0
	});
	var lastYearChart = new Chart(lastYearCTX).LineAlt2(lastYearData, {
		datasetFill: false,
		scaleShowVerticalLines: false,
		datasetStrokeWidth: 5,
		scaleFontColor: '#9e9e9e',
		scaleGridLineColor: '#e4e4e4',
		scaleLineColor: 'transparent',
		scaleOverride: true,
		scaleSteps: 5,
		scaleStepWidth: 20,
		scaleStartValue: 0
	});

	// let ctx = document.getElementById('myChart').getContext('2d');

	// fetch(`${API_BASE}/stock/history/AAPL`)
	// 	.then(response => response.json())
	// 	.then(data => {
	// 		let myLineChart = new Chart(ctx, {
	// 			type: 'line',
	// 			data: {
	// 				labels: data.t,
	// 				datasets: [{
	// 					label: 'Amazon',
	// 					data: data.p,
	// 				}]
	// 			},
	// 			options: {
	// 				responsive: true,
	// 				title: {
	// 					display: true,
	// 					text: 'Portfolio'
	// 				},
	// 				hover: {
	// 					mode: 'nearest',
	// 					intersect: true
	// 				},
	// 				scales: {
	// 					xAxes: [{
	// 						display: true,
	// 						scaleLabel: {
	// 							display: true,
	// 							labelString: 'Time'
	// 						}
	// 					}],
	// 					yAxes: [{
	// 						display: true,
	// 						scaleLabel: {
	// 							display: true,
	// 							labelString: 'Price'
	// 						}
	// 					}]
	// 				}
	// 			}
	// 		});
	// 	});


});

