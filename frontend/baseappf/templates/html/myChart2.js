const myChart2 = document.getElementById('myChart2');

new Chart(ctx, {
  type: 'bar',
  data: dataLine,{
    labels: ['Sheetal R', 'Shantanu K', 'Varsha D', 'Kirti D', 'Swati G', 'Akshata B'],
    datasets: [{
      label: 'Classes Appointed per Teacher per Week',
      data: [24, 36, 29, 25, 30, 33],
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