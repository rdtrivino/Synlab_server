// Toggle Sidebar
document.getElementById('sidebarCollapse').addEventListener('click', function() {
    document.getElementById('sidebar').classList.toggle('active');
    document.getElementById('content').classList.toggle('active');
});

// Update DateTime
function updateDateTime() {
    const now = new Date();
    const options = { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    };
    document.getElementById('currentTime').textContent = now.toLocaleDateString('es-ES', options);
}
setInterval(updateDateTime, 1000);
updateDateTime();

// Charts Configuration
const systemPerformanceChart = new Chart(
    document.getElementById('systemPerformance'),
    {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'CPU',
                    borderColor: '#4e73df',
                    data: []
                },
                {
                    label: 'Memoria',
                    borderColor: '#1cc88a',
                    data: []
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    }
);

const resourcesDonutChart = new Chart(
    document.getElementById('resourcesDonut'),
    {
        type: 'doughnut',
        data: {
            labels: ['CPU', 'Memoria', 'Disco'],
            datasets: [{
                data: [30, 45, 25],
                backgroundColor: ['#4e73df', '#1cc88a', '#f6c23e']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            },
            cutout: '70%'
        }
    }
);

// Función para actualizar los datos (ejemplo)
function updateData() {
    // Aquí deberías obtener los datos reales de tu backend
    const cpuUsage = Math.random() * 100;
    const memoryUsage = Math.random() * 100;
    const diskUsage = Math.random() * 100;
    const networkSpeed = Math.random() * 1000;

    // Actualizar quick stats
    document.getElementById('cpuUsage').textContent = `${cpuUsage.toFixed(1)}%`;
    document.getElementById('memoryUsage').textContent = `${memoryUsage.toFixed(1)}%`;
    document.getElementById('diskUsage').textContent = `${diskUsage.toFixed(1)}%`;
    document.getElementById('networkSpeed').textContent = `${networkSpeed.toFixed(0)} Mb/s`;

    // Actualizar gráficas
    const timestamp = new Date().toLocaleTimeString();
    
    systemPerformanceChart.data.labels.push(timestamp);
    systemPerformanceChart.data.datasets[0].data.push(cpuUsage);
    systemPerformanceChart.data.datasets[1].data.push(memoryUsage);
    
    if (systemPerformanceChart.data.labels.length > 10) {
        systemPerformanceChart.data.labels.shift();
        systemPerformanceChart.data.datasets[0].data.shift();
        systemPerformanceChart.data.datasets[1].data.shift();
    }
    
    systemPerformanceChart.update();
    
    resourcesDonutChart.data.datasets[0].data = [cpuUsage, memoryUsage, diskUsage];
    resourcesDonutChart.update();
}

// Actualizar datos cada 2 segundos
setInterval(updateData, 2000);
updateData(); // Primera actualización 