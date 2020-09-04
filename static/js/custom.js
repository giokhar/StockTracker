const API_BASE = `${window.location.origin}/api`;

const chartColors = ['#9C2E9D', '#0288d1', '#ffca28'];

Chart.types.Line.extend({
	name: "LineAlt",
	initialize: function () {
		Chart.types.Line.prototype.initialize.apply(this, arguments);

		let ctx = this.chart.ctx;
		let originalStroke = ctx.stroke;
		ctx.stroke = function () {
			ctx.save();
			ctx.shadowColor = 'rgba(156, 46, 157,0.5)';
			ctx.shadowBlur = 20;
			ctx.shadowOffsetX = 2;
			ctx.shadowOffsetY = 20;
			originalStroke.apply(this, arguments);
			ctx.restore();
		}
	}
});

Chart.types.Line.extend({
	name: "LineAlt2",
	initialize: function () {
		Chart.types.Line.prototype.initialize.apply(this, arguments);
		let ctx = this.chart.ctx;
		let originalStroke = ctx.stroke;
		ctx.stroke = function () {
			ctx.save();
			originalStroke.apply(this, arguments);
			ctx.restore();
		}
	}
});

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
	// COUNT UP NUMBERS
	countify('#diff_today');
	countify('#current');
	countify('#investment');

	// INITIALIZE MOBILE SIDEBAR
	M.Sidenav.init(document.querySelectorAll('.sidenav'));
	let portfolio_id = document.body.getAttribute('data-p-id');

	fetch(`${API_BASE}/stocks/portfolio/${portfolio_id}`)
		.then(response => response.json())
		.then(portfolio => {
			portfolio.forEach((stock, index) => {
				let ticker = stock.ticker;
				fetch(`${API_BASE}/stock/history/${ticker}`)
					.then(response => response.json())
					.then(stock => {
						let stockCTX = document.getElementById(ticker.toLowerCase()).getContext("2d");
						let stockData = {
							labels: stock.t,
							datasets: [{
								fillColor: chartColors[index],
								strokeColor: chartColors[index],
								pointColor: "transparent",
								pointStrokeColor: "transparent",
								pointHighlightFill: "#fff",
								pointHighlightStroke: chartColors[index],
								data: stock.p
							}]
						};
						let stockChart = new Chart(stockCTX).LineAlt(stockData, {
							datasetFill: false,
							scaleShowGridLines: true,
							datasetStrokeWidth: 5,
							scaleFontColor: '#9e9e9e',
							scaleGridLineColor: '#e4e4e4',
							scaleLineColor: 'transparent',
						});
					});
			})
		});


});

