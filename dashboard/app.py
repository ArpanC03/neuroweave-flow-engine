"""
NeuroWeave Flow Engine - Dashboard Server
Minimal Flask app for post-session analytics
"""

from flask import Flask, render_template, jsonify
import random
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def dashboard():
    """Render main dashboard"""
    return render_template('index.html')

@app.route('/api/session-data')
def get_session_data():
    """Return simulated session data (replace with real DB queries)"""
    
    # Simulate flow score timeline (3-hour session)
    start_time = datetime.now() - timedelta(hours=3)
    timeline = []
    
    for i in range(36):  # 5-min intervals
        timestamp = (start_time + timedelta(minutes=i*5)).strftime('%H:%M')
        
        # Simulate realistic flow curve
        if i < 6:
            score = random.randint(70, 85)  # Warm-up
        elif i < 15:
            score = random.randint(85, 95)  # Peak flow
        elif i < 24:
            score = random.randint(60, 75)  # Decay phase
        else:
            score = random.randint(75, 88)  # Recovery
        
        timeline.append({
            'timestamp': timestamp,
            'score': score
        })
    
    interventions = [
        {'time': '12:30', 'type': 'Stretch Break', 'effective': True},
        {'time': '13:45', 'type': 'Binaural Audio', 'effective': True},
        {'time': '14:20', 'type': 'Micro-break Reminder', 'effective': True}
    ]
    
    return jsonify({
        'timeline': timeline,
        'interventions': interventions,
        'metrics': {
            'peak_flow': 92,
            'avg_flow': 78,
            'total_interventions': 3,
            'time_saved_min': 45
        }
    })

if __name__ == '__main__':
    print("🧠 NeuroWeave Dashboard Server")
    print("📊 Visit: http://localhost:5000")
    app.run(debug=True, port=5000)

