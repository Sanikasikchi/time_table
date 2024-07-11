const ctx = document.getElementById('myChart');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['BSC CS A', 'BSC CS B', 'BCA A', 'BSC IT A', 'BSC IT B'],
      datasets: [{
        label: 'Total Classes Conducted this week',
        data: [4, 6, 2, 5, 3, 3],
        backgroundColor:[
            'rgba(255,99,132,0.3)',
            'rgba(54,162,232,0.3)',
            'rgba(255,206,86,0.3)',
            'rgba(75,192,192,0.3)',
            'rgba(153,102,255,0.3)',
            'rgba(255,159,64,0.3)',
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
    }
  });