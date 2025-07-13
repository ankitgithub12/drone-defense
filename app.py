from flask import Flask, render_template, jsonify, request
from detector import DroneDetector
import threading
from datetime import datetime

app = Flask(__name__)
detector = DroneDetector()

emergency_log = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/status')
def status():
    return jsonify(detector.get_status())

@app.route('/emergency', methods=['POST'])
def emergency():
    timestamp = datetime.now().strftime("%H:%M:%S")
    emergency_log.append(timestamp)
    return jsonify({
        "status": "success",
        "message": f"Emergency alert sent at {timestamp}",
        "siren": True
    })

def run_detector():
    detector.simulate_detection()

if __name__ == '__main__':
    threading.Thread(target=run_detector, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)