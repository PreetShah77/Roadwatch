// Modern Dashboard JavaScript

// Chart.js: Create Bar Chart for Metrics Overview
const barCtx = document.getElementById('barChart').getContext('2d');
let barChart;

// Chart.js: Create Pie Chart for Case Analytics
const pieCtx = document.getElementById('pieChart').getContext('2d');
let pieChart;

// Chart.js: Create Line Chart for Metrics Overview in Right Sidebar
const lineCtx = document.getElementById('lineChart').getContext('2d');
let lineChart;

// Function to initialize charts
function initializeCharts() {
    barChart = new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            datasets: [{
                label: 'Total Cases',
                data: [400, 500, 600, 700, 800, 900, 1000],
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }, {
                label: 'Solved Cases',
                data: [250, 350, 450, 550, 650, 750, 850],
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }, {
                label: 'Pending Cases',
                data: [150, 150, 150, 150, 150, 150, 150],
                backgroundColor: 'rgba(255, 206, 86, 0.6)',
                borderColor: 'rgba(255, 206, 86, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    const solvedCases = 850;
    const pendingCases = 150;

    pieChart = new Chart(pieCtx, {
        type: 'pie',
        data: {
            labels: [
                `Solved Cases: ${solvedCases} (${((solvedCases / (solvedCases + pendingCases)) * 100).toFixed(1)}%)`,
                `Pending Cases: ${pendingCases} (${((pendingCases / (solvedCases + pendingCases)) * 100).toFixed(1)}%)`
            ],
            datasets: [{
                data: [solvedCases, pendingCases],
                backgroundColor: ['#4BC0C0', '#FFCE56'],
            }]
        },
        options: {
            responsive: true,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (tooltipItem) {
                            const data = tooltipItem.dataset.data[tooltipItem.dataIndex];
                            return `${tooltipItem.label}: ${data} cases`;
                        }
                    }
                }
            }
        }
    });

    lineChart = new Chart(lineCtx, {
        type: 'line',
        data: {
            labels: ['2019', '2020', '2021', '2022', '2023'],
            datasets: [{
                label: 'Cases by Year',
                data: [3500, 3700, 4200, 4300, 4500],
                borderColor: 'rgba(75, 192, 192, 1)',
                fill: false,
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Function to update chart data based on time range
function updateChartData(timeRange) {
    let labels, totalCases, solvedCases, pendingCases;

    switch (timeRange) {
        case 'daily':
            labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
            totalCases = [50, 60, 70, 80, 90, 100, 110];
            solvedCases = [30, 40, 50, 60, 70, 80, 90];
            pendingCases = [20, 20, 20, 20, 20, 20, 20];
            break;
        case 'weekly':
            labels = ['Week 1', 'Week 2', 'Week 3', 'Week 4'];
            totalCases = [300, 400, 500, 600];
            solvedCases = [200, 300, 400, 500];
            pendingCases = [100, 100, 100, 100];
            break;
        case 'monthly':
            labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'];
            totalCases = [400, 500, 600, 700, 800, 900, 1000];
            solvedCases = [250, 350, 450, 550, 650, 750, 850];
            pendingCases = [150, 150, 150, 150, 150, 150, 150];
            break;
        case 'yearly':
            labels = ['2019', '2020', '2021', '2022', '2023'];
            totalCases = [3500, 3700, 4200, 4300, 4500];
            solvedCases = [3000, 3200, 3800, 4000, 4200];
            pendingCases = [500, 500, 400, 300, 300];
            break;
    }

    barChart.data.labels = labels;
    barChart.data.datasets[0].data = totalCases;
    barChart.data.datasets[1].data = solvedCases;
    barChart.data.datasets[2].data = pendingCases;
    barChart.update();

    lineChart.data.labels = labels;
    lineChart.data.datasets[0].data = totalCases;
    lineChart.update();

    document.getElementById('casesByYear').textContent = totalCases[totalCases.length - 1];

    // Update metrics overview
    updateMetricsOverview(totalCases, solvedCases, pendingCases);
}

// Function to update metrics overview
function updateMetricsOverview(totalCases, solvedCases, pendingCases) {
    const latestTotal = totalCases[totalCases.length - 1];
    const latestSolved = solvedCases[solvedCases.length - 1];
    const latestPending = pendingCases[pendingCases.length - 1];

    document.getElementById('totalCasesMetric').textContent = latestTotal;
    document.getElementById('solvedCasesMetric').textContent = latestSolved;
    document.getElementById('pendingCasesMetric').textContent = latestPending;

    // Update right sidebar metrics
    document.getElementById('totalCases').textContent = latestTotal;
    document.getElementById('solvedCases').textContent = latestSolved;
    document.getElementById('pendingCases').textContent = latestPending;

    // Calculate priorities (example calculation, adjust as needed)
    const highPriority = Math.round(latestTotal * 0.2);
    const mediumPriority = Math.round(latestTotal * 0.5);
    const lowPriority = latestTotal - highPriority - mediumPriority;

    document.getElementById('highPriorityMetric').textContent = highPriority;
    document.getElementById('mediumPriorityMetric').textContent = mediumPriority;
    document.getElementById('lowPriorityMetric').textContent = lowPriority;

    // Update right sidebar priorities
    document.getElementById('highPriority').textContent = highPriority;
    document.getElementById('mediumPriority').textContent = mediumPriority;
    document.getElementById('lowPriority').textContent = lowPriority;
}

// Function to populate case table
function populateCaseTable() {
    const caseTableBody = document.querySelector('#caseTable tbody');
    const cases = [
        { id: 12345, priority: 'High', status: 'Open', date: '2023-09-15' },
        { id: 67890, priority: 'Medium', status: 'Solved', date: '2023-09-14' },
        { id: 24680, priority: 'Low', status: 'Pending', date: '2023-09-13' },
        { id: 13579, priority: 'High', status: 'Open', date: '2023-09-12' },
        { id: 97531, priority: 'Medium', status: 'Solved', date: '2023-09-11' }
    ];

    caseTableBody.innerHTML = '';
    cases.forEach(caseItem => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${caseItem.id}</td>
            <td>${caseItem.priority}</td>
            <td>${caseItem.status}</td>
            <td>${caseItem.date}</td>
            <td><button class="view-case-btn" data-id="${caseItem.id}">View</button></td>
        `;
        caseTableBody.appendChild(row);
    });
}

// Event listener for time range select
document.getElementById('timeRangeSelect').addEventListener('change', function(event) {
    updateChartData(event.target.value);
});

// Event listener for search button
document.getElementById('searchButton').addEventListener('click', function() {
    const searchTerm = document.getElementById('searchInput').value;
    alert(`Searching for: ${searchTerm}`);
    // Implement actual search functionality here
});

// Event listener for load more cases button
document.getElementById('loadMoreCases').addEventListener('click', function() {
    alert('Loading more cases...');
    // Implement functionality to load more cases here
});

// Event delegation for view case buttons
document.getElementById('caseTable').addEventListener('click', function(event) {
    if (event.target.classList.contains('view-case-btn')) {
        const caseId = event.target.getAttribute('data-id');
        alert(`Viewing case: ${caseId}`);
        // Implement functionality to view case details here
    }
});

// Initialize the dashboard
function initializeDashboard() {
    initializeCharts();
    updateChartData('monthly'); // Default to monthly view
    populateCaseTable();
}

// Call initializeDashboard when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', initializeDashboard);

// Function to initialize charts
function initializeCharts() {
    barChart = new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            datasets: [{
                label: 'Total Cases',
                data: [400, 500, 600, 700, 800, 900, 1000],
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }, {
                label: 'Solved Cases',
                data: [250, 350, 450, 550, 650, 750, 850],
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }, {
                label: 'Pending Cases',
                data: [150, 150, 150, 150, 150, 150, 150],
                backgroundColor: 'rgba(255, 206, 86, 0.6)',
                borderColor: 'rgba(255, 206, 86, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    const solvedCases = 850;
    const pendingCases = 150;

    pieChart = new Chart(pieCtx, {
        type: 'pie',
        data: {
            labels: [
                `Solved Cases: ${solvedCases} (${((solvedCases / (solvedCases + pendingCases)) * 100).toFixed(1)}%)`,
                `Pending Cases: ${pendingCases} (${((pendingCases / (solvedCases + pendingCases)) * 100).toFixed(1)}%)`
            ],
            datasets: [{
                data: [solvedCases, pendingCases],
                backgroundColor: ['#4BC0C0', '#FFCE56'],
            }]
        },
        options: {
            responsive: true,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (tooltipItem) {
                            const data = tooltipItem.dataset.data[tooltipItem.dataIndex];
                            return `${tooltipItem.label}: ${data} cases`;
                        }
                    }
                }
            }
        }
    });

    lineChart = new Chart(lineCtx, {
        type: 'line',
        data: {
            labels: ['2019', '2020', '2021', '2022', '2023'],
            datasets: [{
                label: 'Cases by Year',
                data: [3500, 3700, 4200, 4300, 4500],
                borderColor: 'rgba(75, 192, 192, 1)',
                fill: false,
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Function to update chart data based on time range
function updateChartData(timeRange) {
    let labels, totalCases, solvedCases, pendingCases;

    switch (timeRange) {
        case 'daily':
            labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
            totalCases = [50, 60, 70, 80, 90, 100, 110];
            solvedCases = [30, 40, 50, 60, 70, 80, 90];
            pendingCases = [20, 20, 20, 20, 20, 20, 20];
            break;
        case 'weekly':
            labels = ['Week 1', 'Week 2', 'Week 3', 'Week 4'];
            totalCases = [300, 400, 500, 600];
            solvedCases = [200, 300, 400, 500];
            pendingCases = [100, 100, 100, 100];
            break;
        case 'monthly':
            labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'];
            totalCases = [400, 500, 600, 700, 800, 900, 1000];
            solvedCases = [250, 350, 450, 550, 650, 750, 850];
            pendingCases = [150, 150, 150, 150, 150, 150, 150];
            break;
        case 'yearly':
            labels = ['2019', '2020', '2021', '2022', '2023'];
            totalCases = [3500, 3700, 4200, 4300, 4500];
            solvedCases = [3000, 3200, 3800, 4000, 4200];
            pendingCases = [500, 500, 400, 300, 300];
            break;
    }

    barChart.data.labels = labels;
    barChart.data.datasets[0].data = totalCases;
    barChart.data.datasets[1].data = solvedCases;
    barChart.data.datasets[2].data = pendingCases;
    barChart.update();

    lineChart.data.labels = labels;
    lineChart.data.datasets[0].data = totalCases;
    lineChart.update();

    document.getElementById('casesByYear').textContent = totalCases[totalCases.length - 1];

    // Update metrics overview
    updateMetricsOverview(totalCases, solvedCases, pendingCases);
}

// Function to update metrics overview
function updateMetricsOverview(totalCases, solvedCases, pendingCases) {
    const latestTotal = totalCases[totalCases.length - 1];
    const latestSolved = solvedCases[solvedCases.length - 1];
    const latestPending = pendingCases[pendingCases.length - 1];

    document.getElementById('totalCasesMetric').textContent = latestTotal;
    document.getElementById('solvedCasesMetric').textContent = latestSolved;
    document.getElementById('pendingCasesMetric').textContent = latestPending;

    // Update right sidebar metrics
    document.getElementById('totalCases').textContent = latestTotal;
    document.getElementById('solvedCases').textContent = latestSolved;
    document.getElementById('pendingCases').textContent = latestPending;

    // Calculate priorities (example calculation, adjust as needed)
    const highPriority = Math.round(latestTotal * 0.2);
    const mediumPriority = Math.round(latestTotal * 0.5);
    const lowPriority = latestTotal - highPriority - mediumPriority;

    document.getElementById('highPriorityMetric').textContent = highPriority;
    document.getElementById('mediumPriorityMetric').textContent = mediumPriority;
    document.getElementById('lowPriorityMetric').textContent = lowPriority;

    // Update right sidebar priorities
    document.getElementById('highPriority').textContent = highPriority;
    document.getElementById('mediumPriority').textContent = mediumPriority;
    document.getElementById('lowPriority').textContent = lowPriority;
}

// Function to populate case table
function populateCaseTable() {
    const caseTableBody = document.querySelector('#caseTable tbody');
    const cases = [
        { id: 12345, priority: 'High', status: 'Open', date: '2023-09-15' },
        { id: 67890, priority: 'Medium', status: 'Solved', date: '2023-09-14' },
        { id: 24680, priority: 'Low', status: 'Pending', date: '2023-09-13' },
        { id: 13579, priority: 'High', status: 'Open', date: '2023-09-12' },
        { id: 97531, priority: 'Medium', status: 'Solved', date: '2023-09-11' }
    ];

    caseTableBody.innerHTML = '';
    cases.forEach(caseItem => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${caseItem.id}</td>
            <td>${caseItem.priority}</td>
            <td>${caseItem.status}</td>
            <td>${caseItem.date}</td>
            <td><button class="view-case-btn" data-id="${caseItem.id}">View</button></td>
        `;
        caseTableBody.appendChild(row);
    });
}

// Event listener for time range select
document.getElementById('timeRangeSelect').addEventListener('change', function(event) {
    updateChartData(event.target.value);
});

// Event listener for search button
document.getElementById('searchButton').addEventListener('click', function() {
    const searchTerm = document.getElementById('searchInput').value;
    alert(`Searching for: ${searchTerm}`);
    // Implement actual search functionality here
});

// Event listener for load more cases button
document.getElementById('loadMoreCases').addEventListener('click', function() {
    alert('Loading more cases...');
    // Implement functionality to load more cases here
});

// Event delegation for view case buttons
document.getElementById('caseTable').addEventListener('click', function(event) {
    if (event.target.classList.contains('view-case-btn')) {
        const caseId = event.target.getAttribute('data-id');
        alert(`Viewing case: ${caseId}`);
        // Implement functionality to view case details here
    }
});