// Initialize Lucide Icons
lucide.createIcons();

// Page Navigation
function showPage(pageId) {
    document.querySelectorAll('main > div').forEach(div => div.classList.add('hidden'));
    document.getElementById('page-' + pageId).classList.remove('hidden');
    
    document.querySelectorAll('.sidebar-item').forEach(btn => btn.classList.remove('active'));
    
    // Set active class on clicked button
    const currentBtn = Array.from(document.querySelectorAll('.sidebar-item'))
        .find(btn => btn.getAttribute('onclick').includes(pageId));
    if (currentBtn) currentBtn.classList.add('active');

    const titles = {
        'home': 'Risk Intelligence Overview',
        'upload': 'Invoice Forensic Analysis',
        'vendors': 'Vendor Intelligence Network',
        'alerts': 'Critical Threat Monitor',
        'reports': 'Risk Mitigation Reports'
    };
    document.getElementById('page-title').innerText = titles[pageId];
}

// --- Charts Configuration ---

// Line Chart
const trendCtx = document.getElementById('trendChart').getContext('2d');
new Chart(trendCtx, {
    type: 'line',
    data: {
        labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
        datasets: [{
            label: 'Anomalies',
            data: [12, 19, 3, 5, 25, 10],
            borderColor: '#3b82f6',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            fill: true,
            tension: 0.4,
            borderWidth: 3,
            pointRadius: 0
        }, {
            label: 'Total Invoices',
            data: [100, 150, 120, 180, 250, 220],
            borderColor: 'rgba(255,255,255,0.2)',
            fill: false,
            tension: 0.4,
            borderDash: [5, 5],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
            y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#64748b' } },
            x: { grid: { display: false }, ticks: { color: '#64748b' } }
        }
    }
});

// Pie Chart
const riskCtx = document.getElementById('riskPieChart').getContext('2d');
new Chart(riskCtx, {
    type: 'doughnut',
    data: {
        labels: ['High', 'Medium', 'Low'],
        datasets: [{
            data: [12, 16, 72],
            backgroundColor: ['#ef4444', '#f59e0b', '#10b981'],
            borderWidth: 0,
            hoverOffset: 10
        }]
    },
    options: {
        cutout: '80%',
        plugins: { legend: { display: false } }
    }
});

// --- Animations & Simulations ---

// Counters Animation
const counters = document.querySelectorAll('.counter');
counters.forEach(counter => {
    const target = +counter.getAttribute('data-target');
    const duration = 2000;
    const increment = target / (duration / 16);
    let current = 0;

    const updateCounter = () => {
        current += increment;
        if (current < target) {
            counter.innerText = Math.ceil(current).toLocaleString();
            requestAnimationFrame(updateCounter);
        } else {
            counter.innerText = target.toLocaleString();
        }
    };
    updateCounter();
});

// Live Log Simulation
const logContainer = document.getElementById('live-logs');
const logsData = [
    { text: "Analyzing metadata for Invoice #4402...", color: "text-gray-400" },
    { text: "Cross-referencing vendor 'Apex Corp'...", color: "text-gray-400" },
    { text: "MATCH DETECTED: Bank routing changed.", color: "text-red-400" },
    { text: "Flagging Invoice #4402 for review.", color: "text-yellow-400" },
    { text: "OCR extraction complete.", color: "text-blue-400" },
    { text: "System integrity check: 100% OK", color: "text-green-500" }
];

function addLog() {
    if(!logContainer) return;
    const log = logsData[Math.floor(Math.random() * logsData.length)];
    const div = document.createElement('div');
    div.className = `flex gap-2 ${log.color}`;
    div.innerHTML = `<span class="text-blue-500/50">[${new Date().toLocaleTimeString()}]</span> <span>${log.text}</span>`;
    logContainer.prepend(div);
    if (logContainer.children.length > 10) logContainer.lastChild.remove();
}
setInterval(addLog, 3000);

// Upload Simulation
function simulateUpload() {
    const scanLine = document.getElementById('scan-line');
    const placeholder = document.getElementById('upload-placeholder');
    const result = document.getElementById('analysis-result');
    
    scanLine.style.display = 'block';
    
    setTimeout(() => {
        scanLine.style.display = 'none';
        placeholder.classList.add('hidden');
        result.classList.remove('hidden');
        result.classList.add('animate-pulse');
        setTimeout(() => result.classList.remove('animate-pulse'), 1000);
    }, 3000);
}