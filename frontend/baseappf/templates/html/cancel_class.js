const ctx = document.getElementById('myChart');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['BSC CS A', 'BSC IT A', 'BCS IT B', 'BCA B', 'BCA B'],
      datasets: [{
        label: 'Classes Cancelled per Week per Class',
        data: [2, 3, 2, 2, 3],
        backgroundColor:[
            'rgba(255,99,132,0.3)',
            'rgba(54,162,232,0.3)',
            'rgba(255,206,86,0.3)',
            'rgba(75,192,192,0.3)',
            'rgba(153,102,255,0.3)',
            'rgba(255,159,64,0.3)',
        ],
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
    }
  });