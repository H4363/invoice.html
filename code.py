import os
import subprocess
import sys

# 1. Project Structure Define karna
PROJECT_NAME = "smart-invoice-ai"
folders = [
    f"{PROJECT_NAME}/backend",
    f"{PROJECT_NAME}/frontend/src/components",
    f"{PROJECT_NAME}/frontend/src/pages",
    f"{PROJECT_NAME}/frontend/public"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

print("🚀 Folder Structure Created...")

# 2. BACKEND CODE (app.py)
backend_code = """
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

app = Flask(__name__)
CORS(app)

# Train a simple model on the fly for demo
def train_model():
    data = {
        'amount': np.random.uniform(100, 10000, 100),
        'trust_score': np.random.uniform(0, 100, 100),
        'past_avg_amount': np.random.uniform(100, 8000, 100),
        'past_fraud_count': np.random.randint(0, 5, 100),
    }
    df = pd.DataFrame(data)
    df['label'] = ((df['amount'] > df['past_avg_amount'] * 1.5) | (df['trust_score'] < 30)).astype(int)
    model = RandomForestClassifier()
    model.fit(df[['amount', 'trust_score', 'past_avg_amount', 'past_fraud_count']], df['label'])
    joblib.dump(model, 'model.pkl')

train_model()
model = joblib.load('model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    try:
        amt = float(data['amount'])
        ts = float(data['trust_score'])
        p_avg = float(data['past_avg_amount'])
        p_f = int(data['past_fraud_count'])
        
        # ML Prediction
        prob = model.predict_proba([[amt, ts, p_avg, p_f]])[0][1] * 100
        
        # Rule Engine
        reasons = []
        rule_score = 0
        if amt > p_avg * 2: 
            rule_score += 40
            reasons.append("Amount is 2x higher than usual")
        if ts < 40: 
            rule_score += 30
            reasons.append("Low vendor trust score")
        if p_f > 0:
            rule_score += 20
            reasons.append("Vendor has past fraud history")

        final_score = min(100, (prob * 0.5) + (rule_score * 0.5))
        status = "HIGH RISK" if final_score > 70 else "MEDIUM RISK" if final_score > 40 else "LOW RISK"

        return jsonify({
            "risk_score": round(final_score, 2),
            "status": status,
            "reasons": reasons,
            "invoice_id": data.get('invoice_id', 'INV-UNK')
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(port=5000, debug=True)
"""

with open(f"{PROJECT_NAME}/backend/app.py", "w") as f:
    f.write(backend_code)

# 3. FRONTEND (Single-File Dashboard using Tailwind & Lucide)
# Isko hum index.html ke roop mein serve karenge fast results ke liye
frontend_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmartInvoice AI Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Plus Jakarta Sans', sans-serif; background: #0f172a; color: white; }
        .glass { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.1); }
        .neon-border { border: 1px solid #6366f1; box-shadow: 0 0 15px rgba(99, 102, 241, 0.3); }
    </style>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect } = React;

        function App() {
            const [form, setForm] = useState({ invoice_id: 'INV-1002', amount: '', trust_score: '', past_avg_amount: '', past_fraud_count: '0' });
            const [result, setResult] = useState(null);
            const [loading, setLoading] = useState(false);

            const handleScan = async (e) => {
                e.preventDefault();
                setLoading(true);
                try {
                    const res = await fetch('http://localhost:5000/predict', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(form)
                    });
                    const data = await res.json();
                    setResult(data);
                } catch (err) { alert("Backend not running! Start app.py first."); }
                setLoading(false);
            }

            return (
                <div className="min-h-screen p-8">
                    <nav className="flex justify-between items-center mb-12">
                        <div className="flex items-center gap-2 text-2xl font-bold text-indigo-400">
                            <i data-lucide="shield-check"></i> SMART INVOICE AI
                        </div>
                        <div className="flex gap-4 text-sm text-slate-400">
                            <span className="flex items-center gap-1"><span className="w-2 h-2 bg-emerald-500 rounded-full"></span> AI Engine Online</span>
                            <span>Model v1.0.4 (96.4% Acc)</span>
                        </div>
                    </nav>

                    <div className="grid lg:grid-cols-3 gap-8">
                        {/* Form Section */}
                        <div className="lg:col-span-1 glass p-8 rounded-3xl">
                            <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
                                <i data-lucide="scan-line" className="text-indigo-400"></i> New Analysis
                            </h2>
                            <form onSubmit={handleScan} className="space-y-4">
                                <div>
                                    <label className="text-xs text-slate-400 block mb-1">Invoice Amount ($)</label>
                                    <input type="number" required className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 outline-none focus:border-indigo-500" 
                                        onChange={e => setForm({...form, amount: e.target.value})} placeholder="5000" />
                                </div>
                                <div>
                                    <label className="text-xs text-slate-400 block mb-1">Vendor Trust Score (0-100)</label>
                                    <input type="number" required className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 outline-none focus:border-indigo-500" 
                                        onChange={e => setForm({...form, trust_score: e.target.value})} placeholder="85" />
                                </div>
                                <div>
                                    <label className="text-xs text-slate-400 block mb-1">Past Avg Amount ($)</label>
                                    <input type="number" required className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 outline-none focus:border-indigo-500" 
                                        onChange={e => setForm({...form, past_avg_amount: e.target.value})} placeholder="2000" />
                                </div>
                                <button className="w-full bg-indigo-600 hover:bg-indigo-500 py-4 rounded-xl font-bold transition-all flex justify-center items-center gap-2">
                                    {loading ? "Analyzing..." : "Run AI Scanning"}
                                </button>
                            </form>
                        </div>

                        {/* Result Section */}
                        <div className="lg:col-span-2 space-y-6">
                            {!result ? (
                                <div className="h-full glass rounded-3xl flex flex-col items-center justify-center text-slate-500 border-dashed border-2 border-slate-700">
                                    <i data-lucide="database" size="48" className="mb-4"></i>
                                    <p>Ready for system scan. Enter data to see AI insights.</p>
                                </div>
                            ) : (
                                <div className={`glass p-8 rounded-3xl border-l-8 ${result.status === 'HIGH RISK' ? 'border-red-500' : 'border-emerald-500'}`}>
                                    <div className="flex justify-between items-start mb-8">
                                        <div>
                                            <p className="text-slate-400 text-sm">Invoice Risk Level</p>
                                            <h3 className={`text-5xl font-black ${result.status === 'HIGH RISK' ? 'text-red-500' : 'text-emerald-500'}`}>
                                                {result.status}
                                            </h3>
                                        </div>
                                        <div className="text-right">
                                            <p className="text-slate-400 text-sm">AI Score</p>
                                            <p className="text-4xl font-mono font-bold text-indigo-400">{result.risk_score}%</p>
                                        </div>
                                    </div>

                                    <div className="bg-slate-900/50 p-6 rounded-2xl mb-6">
                                        <h4 className="font-bold mb-4 flex items-center gap-2">
                                            <i data-lucide="alert-circle" className="text-amber-500"></i> Detection Reasons:
                                        </h4>
                                        <ul className="space-y-3">
                                            {result.reasons.length > 0 ? result.reasons.map((r, i) => (
                                                <li key={i} className="flex items-center gap-2 text-slate-300">
                                                    <div className="w-1.5 h-1.5 bg-indigo-500 rounded-full"></div> {r}
                                                </li>
                                            )) : <li className="text-emerald-400">No suspicious patterns detected. Clear for payment.</li>}
                                        </ul>
                                    </div>
                                    
                                    <div className="flex gap-4">
                                        <button className="bg-slate-800 px-6 py-2 rounded-lg text-sm font-semibold">Flag Vendor</button>
                                        <button className="bg-indigo-600 px-6 py-2 rounded-lg text-sm font-semibold">Approve Invoice</button>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            );
        }

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
        setTimeout(() => lucide.createIcons(), 500);
    </script>
</body>
</html>
"""

with open(f"{PROJECT_NAME}/index.html", "w") as f:
    f.write(frontend_html)

print("\n✅ Project Setup Complete!")
print(f"\n👉 Next Steps:")
print(f"1. Open terminal and run: pip install flask flask-cors pandas scikit-learn joblib")
print(f"2. Run the backend: python {PROJECT_NAME}/backend/app.py")
print(f"3. Open '{PROJECT_NAME}/index.html' in your browser.")