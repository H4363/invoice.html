// Initialize Lucide Icons
lucide.createIcons();

// 1. Nagpur Fraud Detection Simulation
function startFraudDetection() {
    const logs = document.getElementById('geo-logs');
    const target = document.getElementById('nagpur-target');
    const path = document.getElementById('threat-path');

    const addLog = (text, type = 'info') => {
        const div = document.createElement('div');
        const color = type === 'danger' ? 'text-red-500 font-bold' : (type === 'success' ? 'text-cyan-400' : 'text-gray-500');
        div.className = color;
        div.innerHTML = `[${new Date().toLocaleTimeString()}] ${text}`;
        logs.prepend(div);
    };

    // Simulation Sequence
    addLog("Inbound Invoice Payload detected from Node: 172.16.0.4...", 'info');
    
    setTimeout(() => {
        addLog("Neural cross-check: Vendor ID 9928 does not match footprint.", 'info');
        gsap.to(path, { opacity: 0.5, duration: 1 });
    }, 1000);

    setTimeout(() => {
        addLog("CRITICAL: IBAN manipulation attempt detected via Proxy.", 'danger');
        // Pointing to Nagpur
        target.classList.remove('hidden');
        gsap.from(target, { scale: 3, opacity: 0, duration: 1, ease: "expo.out" });
    }, 2500);

    setTimeout(() => {
        addLog("LOCATION LOCKED: Nagpur, Maharashtra (21.1458° N, 79.0882° E)", 'danger');
        addLog("FRAUD INTERCEPTED. System state: PROTECTED.", 'success');
    }, 4000);
}

// 2. Initialize Map Path Animation with GSAP
gsap.to(".path-active", {
    strokeDashoffset: 0,
    duration: 4,
    repeat: -1,
    ease: "linear"
});

// 3. Background Terminal Logic Simulation
setInterval(() => {
    const log = document.getElementById('geo-logs');
    if(log && Math.random() > 0.7) {
        const div = document.createElement('div');
        div.className = "text-[8px] text-cyan-900 mono";
        div.innerText = `PING: Packet_Loss_${(Math.random()*0.1).toFixed(4)}% at Node_Nagpur_Internal`;
        log.prepend(div);
        if (log.children.length > 20) log.removeChild(log.lastChild);
    }
}, 500);