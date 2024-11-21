document.addEventListener("DOMContentLoaded", function () {
    // Fetch KPI completion data for all users
    fetch('/api/kpi-completion-all-users/')
      .then(response => response.json())
      .then(data => {
        var cycleLabels = data[Object.keys(data)[0]].cycle_labels;  // Get review cycles
        var datasets = [];
  
        // Loop through each user and prepare a dataset for the chart
        for (var username in data) {
          var userKpiTrend = data[username].kpi_trend;
          datasets.push({
            label: username,
            fill: true,
            backgroundColor: 'rgba(72,72,176,0.2)',
            borderColor: '#d048b6',
            borderWidth: 2,
            pointBackgroundColor: '#d048b6',
            pointRadius: 4,
            data: userKpiTrend
          });
        }
  
        // Create the bar chart for KPI Comparison
        var ctx = document.getElementById("chartLinePurple").getContext("2d");
        var chartData = {
          labels: cycleLabels,  // X-axis labels (review cycles)
          datasets: datasets    // KPI data for each user
        };
  
        var myChart = new Chart(ctx, {
          type: 'bar',  // Change to bar chart
          data: chartData,
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                beginAtZero: true
              }
            },
            plugins: {
              legend: {
                position: 'top',
              }
            }
          }
        });
      })
      .catch(error => console.error('Error fetching KPI completion data:', error));
  
      fetch('/api/employee-kpi-performance/')
      .then(response => response.json())
      .then(data => {
        // Prepare labels and datasets for the chart
        var cycleLabels = Object.keys(data); // Review cycles (X-axis)
        var kpiNames = [...new Set(Object.values(data).flatMap(Object.keys))]; // Unique KPI names
        var datasets = [];
        
        // Generate a unique color for each bar
        function generateColor(index) {
          const colors = [
            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', 
            '#9966FF', '#FF9F40', '#FF4500', '#228B22', 
            '#FFD700', '#00CED1', '#DC143C', '#8A2BE2'
          ]; // Predefined vibrant colors
          return colors[index % colors.length]; // Cycle through colors
        }
  
        // Loop through each KPI and prepare a dataset
        kpiNames.forEach((kpi, index) => {
          var kpiData = cycleLabels.map(cycle => data[cycle][kpi] || 0); // Performance for each cycle
  
          datasets.push({
            label: kpi,
            data: kpiData,
            backgroundColor: kpiData.map((_, i) => generateColor(i)), // Unique color for each bar
            borderColor: generateColor(index), // Border color matches the bar
            borderWidth: 1,
          });
        });
  
        // Create the bar chart
        var ctx = document.getElementById("CountryChart").getContext("2d");
        var chartData = {
          labels: cycleLabels, // X-axis labels (review cycles)
          datasets: datasets   // KPI performance data
        };
  
        var myChart = new Chart(ctx, {
          type: 'bar',  // Bar chart
          data: chartData,
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              x: {
                stacked: false // Separate bars for better visibility
              },
              y: {
                beginAtZero: true,
                title: {
                  display: true,
                  text: 'Average Performance'
                }
              }
            },
            plugins: {
              legend: {
                position: 'top',
              },
              tooltip: {
                callbacks: {
                  label: function(tooltipItem) {
                    return `${tooltipItem.dataset.label}: ${tooltipItem.raw.toFixed(2)}`;
                  }
                }
              }
            }
          }
        });
      })
      .catch(error => console.error('Error fetching employee KPI performance data:', error));
  
      fetch('/api/employee-performance-trend/')
      .then(response => response.json())
      .then(data => {
        var cycleLabels = data.cycle_labels;  // Get review cycles from the response
        var performanceTrend = data.performance_trend;  // Get the average performance trend for all employees
  
        // Prepare the dataset for the chart (only one line)
        var dataset = {
          label: 'Average Performance',
          data: performanceTrend,  // Use the averaged performance values
          fill: false,  // Line chart with no fill under the line
          borderColor: '#00c5dc',  // Line color
          tension: 0.1,  // Controls the smoothness of the line
          borderWidth: 2
        };
  
        // Create the line chart for Employee Performance Trend
        var ctx = document.getElementById("chartEPT").getContext("2d");
        var chartData = {
          labels: cycleLabels,  // X-axis labels (review cycles)
          datasets: [dataset]    // Only one dataset for the average performance
        };
  
        var myChart = new Chart(ctx, {
          type: 'line',  // Line chart
          data: chartData,
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                beginAtZero: true,  // Ensure the Y-axis starts at 0
                title: {
                  display: true,
                  text: 'Average Performance'
                }
              }
            },
            plugins: {
              legend: {
                position: 'top',
              },
              tooltip: {
                callbacks: {
                  label: function(tooltipItem) {
                    return 'Performance: ' + tooltipItem.raw.toFixed(2);  // Show average with 2 decimal places
                  }
                }
              }
            }
          }
        });
      })
      .catch(error => console.error('Error fetching employee performance trend data:', error));
  });
// Fetch the data for KPI performance pie chart
fetch('/api/kpi-performance-pie-chart/')
.then(response => response.json())
.then(data => {
  // Prepare the data for the pie chart
  var chartData = {
    labels: ['Exceeded', 'Met', 'Underperformed'],
    datasets: [{
      data: [data.exceeded, data.met, data.underperformed],
      backgroundColor: ['#4caf50', '#ffeb3b', '#f44336'],  // Green, Yellow, Red colors
      borderWidth: 1
    }]
  };

  // Get the chart context
  var ctx = document.getElementById("kpiPerformancePieChart").getContext("2d");

  // Create the pie chart
  var myChart = new Chart(ctx, {
    type: 'pie',  // Pie chart
    data: chartData,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
        },
        tooltip: {
          callbacks: {
            label: function(tooltipItem) {
              return tooltipItem.label + ': ' + tooltipItem.raw + ' employees';
            }
          }
        }
      }
    }
  });
})
.catch(error => console.error('Error fetching KPI performance data:', error));