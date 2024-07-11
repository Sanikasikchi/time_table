var ctx = document.getElementById('myChart').getContext('2d');
var myChart2 = document.getElementById('myChart2').getContext('2d');
var myChart3 = document.getElementById('myChart3').getContext('2d');
var myChart4 = document.getElementById('myChart4').getContext('2d');
var myChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['BSC CS A', 'BSC CS B', 'BSC IT A', 'BSC IT B', 'BCA A', 'BCA B'],
    datasets: [{
      label: 'Teachers per Class:',
      data: [5, 4, 4, 4, 8, 7],
      backgroundColor: [
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

var myChart = new Chart(myChart2, {
  type: 'bar',
  data: {
    labels: ['BSC CS A', 'BSC CS B', 'BSC IT A', 'BSC IT B', 'BCA A', 'BCA B'],
    datasets: [{
      label: 'Visitnng Faculty per Class:',
      data: [2, 1, 2, 1, 1, 3],
      backgroundColor: [
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
    indexAxis: 'y',
  }
});

var myChart = new Chart(myChart3, {
  type: 'bar',
  data: {
    labels: ['Sheetal R', 'Shantanu K', 'Varsha D', 'Kirti D', 'Swati G', 'Akshata B'],
    datasets: [{
      label: 'Classes Coudected per Month:',
      data: [35, 28, 38, 40, 25, 34],
      backgroundColor: [
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
    indexAxis: 'y',
  }
});

var myChart = new Chart(myChart4, {
  type: 'line',
  data: {
    labels: ['January', 'February', 'March', 'April', 'Friday', 'May'],
    datasets: [{
      label: 'Holidays per Month:',
      data: [8, 3, 10, 5, 4, 3],
      backgroundColor: [
        'rgba(255,99,132,1)',
        'rgba(54,162,232,1)',
        'rgba(255,206,86,1)',
        'rgba(75,192,192,1)',
        'rgba(153,102,255,1)',
        'rgba(255,159,64,1)',
      ],
      borderWidth: 1
    }]
  },
  options: {
    responsive: true,
  }
});