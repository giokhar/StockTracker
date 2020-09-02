const API_BASE = `${window.location.origin}/api`;

window.addEventListener("DOMContentLoaded", () => {

	let ctx = document.getElementById('myChart').getContext('2d');

	fetch(`${API_BASE}/stock/history/AAPL`)
		.then(response => response.json())
		.then(data => {
			let myLineChart = new Chart(ctx, {
				type: 'line',
				data: {
					labels: data.t,
					datasets: [{
						label: 'Amazon',
						data: data.p,
					}]
				},
				options: {
					responsive: true,
					title: {
						display: true,
						text: 'Portfolio'
					},
					hover: {
						mode: 'nearest',
						intersect: true
					},
					scales: {
						xAxes: [{
							display: true,
							scaleLabel: {
								display: true,
								labelString: 'Time'
							}
						}],
						yAxes: [{
							display: true,
							scaleLabel: {
								display: true,
								labelString: 'Price'
							}
						}]
					}
				}
			});
		});


});

