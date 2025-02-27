// admin-dshboard.js
const barCtx = document.getElementById('barChart').getContext('2d');
const pieCtx = document.getElementById('pieChart').getContext('2d');
const lineCtx = document.getElementById('lineChart').getContext('2d');
const doughnutCtx = document.getElementById('doughnutChart').getContext('2d');

let barChart, pieChart, lineChart, doughnutChart;
let currentPage = 1;
const casesPerPage = 5;

async function fetchDashboardData(timeRange, location, status, severity, page = 1) {
    const url = new URL('/get_dashboard_data/', window.location.origin);
    url.searchParams.append('timeRange', timeRange);
    if (location) url.searchParams.append('location', location);
    if (status) url.searchParams.append('status', status);
    if (severity) url.searchParams.append('severity', severity);
    url.searchParams.append('page', page);
    url.searchParams.append('limit', casesPerPage);

    const response = await fetch(url, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    });
    return await response.json();
}

function initializeCharts(data) {
    barChart = new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: data.chartData.labels,
            datasets: [
                { label: 'Total Cases', data: data.chartData.totalCases, backgroundColor: '#4F46E5', borderColor: '#4338CA', borderWidth: 1, borderRadius: 5 },
                { label: 'Solved Cases', data: data.chartData.solvedCases, backgroundColor: '#10B981', borderColor: '#0d8f68', borderWidth: 1, borderRadius: 5 },
                { label: 'Pending Cases', data: data.chartData.pendingCases, backgroundColor: '#F97316', borderColor: '#e66a14', borderWidth: 1, borderRadius: 5 }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { 
                    beginAtZero: true,
                    grid: { color: '#E5E7EB' },
                    ticks: { color: '#374151', font: { size: 12, family: 'Poppins' } }
                },
                x: { 
                    grid: { display: false },
                    ticks: { color: '#374151', font: { size: 12, family: 'Poppins' } }
                }
            },
            plugins: {
                legend: { 
                    position: 'top',
                    labels: { color: '#374151', font: { size: 14, family: 'Poppins' } }
                },
                tooltip: { 
                    backgroundColor: '#1F2937',
                    titleFont: { size: 14, family: 'Poppins' },
                    bodyFont: { size: 12, family: 'Poppins' }
                }
            }
        }
    });

    pieChart = new Chart(pieCtx, {
        type: 'pie',
        data: {
            labels: [
                `Solved: ${data.pieChartData.solvedCases} (${((data.pieChartData.solvedCases / (data.pieChartData.solvedCases + data.pieChartData.pendingCases)) * 100).toFixed(1)}%)`,
                `Pending: ${data.pieChartData.pendingCases} (${((data.pieChartData.pendingCases / (data.pieChartData.solvedCases + data.pieChartData.pendingCases)) * 100).toFixed(1)}%)`
            ],
            datasets: [{
                data: [data.pieChartData.solvedCases, data.pieChartData.pendingCases],
                backgroundColor: ['#10B981', '#F97316'],
                borderColor: ['#0d8f68', '#e66a14'],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { 
                    position: 'bottom',
                    labels: { color: '#374151', font: { size: 14, family: 'Poppins' } }
                },
                tooltip: { 
                    backgroundColor: '#1F2937',
                    titleFont: { size: 14, family: 'Poppins' },
                    bodyFont: { size: 12, family: 'Poppins' }
                }
            }
        }
    });

    lineChart = new Chart(lineCtx, {
        type: 'line',
        data: {
            labels: data.chartData.labels,
            datasets: [{
                label: 'Total Cases Over Time',
                data: data.chartData.totalCases,
                borderColor: '#4F46E5',
                backgroundColor: 'rgba(79, 70, 229, 0.1)',
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#4F46E5',
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { 
                    beginAtZero: true,
                    grid: { color: '#E5E7EB' },
                    ticks: { color: '#374151', font: { size: 12, family: 'Poppins' } }
                },
                x: { 
                    grid: { display: false },
                    ticks: { color: '#374151', font: { size: 12, family: 'Poppins' } }
                }
            },
            plugins: {
                legend: { 
                    position: 'top',
                    labels: { color: '#374151', font: { size: 14, family: 'Poppins' } }
                },
                tooltip: { 
                    backgroundColor: '#1F2937',
                    titleFont: { size: 14, family: 'Poppins' },
                    bodyFont: { size: 12, family: 'Poppins' }
                }
            }
        }
    });

    doughnutChart = new Chart(doughnutCtx, {
        type: 'doughnut',
        data: {
            labels: ['High', 'Medium', 'Low'],
            datasets: [{
                data: [data.metrics.highPriority, data.metrics.mediumPriority, data.metrics.lowPriority],
                backgroundColor: ['#EF4444', '#FBBF24', '#3498DB'],
                borderColor: ['#d63c3c', '#e6ac20', '#2e88c8'],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '60%', // Makes it a thinner doughnut
            plugins: {
                legend: { 
                    position: 'bottom',
                    labels: { color: '#374151', font: { size: 14, family: 'Poppins' } }
                },
                tooltip: { 
                    backgroundColor: '#1F2937',
                    titleFont: { size: 14, family: 'Poppins' },
                    bodyFont: { size: 12, family: 'Poppins' }
                }
            }
        }
    });
}

function updateDashboard(data, append = false) {
    barChart.data.labels = data.chartData.labels;
    barChart.data.datasets[0].data = data.chartData.totalCases;
    barChart.data.datasets[1].data = data.chartData.solvedCases;
    barChart.data.datasets[2].data = data.chartData.pendingCases;
    barChart.update();

    pieChart.data.labels = [
        `Solved: ${data.pieChartData.solvedCases} (${((data.pieChartData.solvedCases / (data.pieChartData.solvedCases + data.pieChartData.pendingCases)) * 100).toFixed(1)}%)`,
        `Pending: ${data.pieChartData.pendingCases} (${((data.pieChartData.pendingCases / (data.pieChartData.solvedCases + data.pieChartData.pendingCases)) * 100).toFixed(1)}%)`
    ];
    pieChart.data.datasets[0].data = [data.pieChartData.solvedCases, data.pieChartData.pendingCases];
    pieChart.update();

    lineChart.data.labels = data.chartData.labels;
    lineChart.data.datasets[0].data = data.chartData.totalCases;
    lineChart.update();

    doughnutChart.data.datasets[0].data = [data.metrics.highPriority, data.metrics.mediumPriority, data.metrics.lowPriority];
    doughnutChart.update();

    document.getElementById('totalCasesMetric').textContent = data.metrics.totalCases;
    document.getElementById('solvedCasesMetric').textContent = data.metrics.solvedCases;
    document.getElementById('pendingCasesMetric').textContent = data.metrics.pendingCases;
    document.getElementById('highPriorityMetric').textContent = data.metrics.highPriority;
    document.getElementById('mediumPriorityMetric').textContent = data.metrics.mediumPriority;
    document.getElementById('lowPriorityMetric').textContent = data.metrics.lowPriority;

    document.getElementById('totalCases').textContent = data.metrics.totalCases;
    document.getElementById('solvedCases').textContent = data.metrics.solvedCases;
    document.getElementById('pendingCases').textContent = data.metrics.pendingCases;
    document.getElementById('highPriority').textContent = data.metrics.highPriority;
    document.getElementById('mediumPriority').textContent = data.metrics.mediumPriority;
    document.getElementById('lowPriority').textContent = data.metrics.lowPriority;

    const caseTableBody = document.querySelector('#caseTable tbody');
    if (!append) caseTableBody.innerHTML = '';
    data.recentCases.forEach(caseItem => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${caseItem.complaint_id}</td>
            <td>${caseItem.severity}</td>
            <td>${caseItem.status}</td>
            <td>${new Date(caseItem.timestamp).toLocaleDateString()}</td>
            <td><button class="view-case-btn" data-id="${caseItem.complaint_id}">View</button></td>
        `;
        caseTableBody.appendChild(row);
    });
}

async function loadMoreCases() {
    const timeRange = document.getElementById('timeRangeSelect').value;
    const location = document.getElementById('searchInput').value;
    const status = document.getElementById('statusFilter').value;
    const severity = document.getElementById('severityFilter').value;
    currentPage++;
    const data = await fetchDashboardData(timeRange, location, status, severity, currentPage);
    if (data.recentCases.length > 0) {
        updateDashboard(data, true);
    } else {
        alert('No more cases to load.');
        currentPage--;
    }
}

document.getElementById('timeRangeSelect').addEventListener('change', async () => {
    currentPage = 1;
    const data = await fetchDashboardData(
        document.getElementById('timeRangeSelect').value,
        document.getElementById('searchInput').value,
        document.getElementById('statusFilter').value,
        document.getElementById('severityFilter').value
    );
    updateDashboard(data);
});

document.getElementById('searchButton').addEventListener('click', async () => {
    currentPage = 1;
    const data = await fetchDashboardData(
        document.getElementById('timeRangeSelect').value,
        document.getElementById('searchInput').value,
        document.getElementById('statusFilter').value,
        document.getElementById('severityFilter').value
    );
    updateDashboard(data);
});

document.getElementById('statusFilter').addEventListener('change', async () => {
    currentPage = 1;
    const data = await fetchDashboardData(
        document.getElementById('timeRangeSelect').value,
        document.getElementById('searchInput').value,
        document.getElementById('statusFilter').value,
        document.getElementById('severityFilter').value
    );
    updateDashboard(data);
});

document.getElementById('severityFilter').addEventListener('change', async () => {
    currentPage = 1;
    const data = await fetchDashboardData(
        document.getElementById('timeRangeSelect').value,
        document.getElementById('searchInput').value,
        document.getElementById('statusFilter').value,
        document.getElementById('severityFilter').value
    );
    updateDashboard(data);
});

document.getElementById('exportExcelButton').addEventListener('click', () => {
    const timeRange = document.getElementById('timeRangeSelect').value;
    const location = document.getElementById('searchInput').value;
    const status = document.getElementById('statusFilter').value;
    const severity = document.getElementById('severityFilter').value;
    const url = `/export_to_excel/?timeRange=${timeRange}&location=${location}&status=${status}&severity=${severity}`;
    window.location.href = url;
});

document.getElementById('loadMoreCases').addEventListener('click', loadMoreCases);

document.getElementById('caseTable').addEventListener('click', (event) => {
    if (event.target.classList.contains('view-case-btn')) {
        const caseId = event.target.getAttribute('data-id');
        alert(`Viewing case: ${caseId}`);
    }
});

async function initializeDashboard() {
    const initialData = await fetchDashboardData('monthly', '', '', '', 1);
    initializeCharts(initialData);
    updateDashboard(initialData);
}

document.addEventListener('DOMContentLoaded', initializeDashboard);