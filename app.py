from flask import Flask, render_template, jsonify, send_from_directory
from detector import DroneDetector
import threading
from datetime import datetime

app = Flask(__name__, static_folder='static', template_folder='templates')

# Initialize detector
detector = DroneDetector()
emergency_log = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/status')
def status():
    try:
        return jsonify(detector.get_status())
    except Exception as e:
        print(f"Status error: {str(e)}")
        return jsonify({"error": "Server error"}), 500

@app.route('/emergency', methods=['POST'])
def emergency():
    timestamp = datetime.now().strftime("%H:%M:%S")
    emergency_log.append(timestamp)
    return jsonify({
        "status": "success",
        "message": f"Emergency alert sent at {timestamp}",
        "siren": True
    })

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/health')
def health():
    return 'OK', 200

def run_detector():
    detector.simulate_detection()

if __name__ == '__main__':
    threading.Thread(target=run_detector, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)