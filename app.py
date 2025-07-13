from flask import Flask, jsonify, send_from_directory, render_template
from detector import DroneDetector
import threading
import time
from datetime import datetime

app = Flask(__name__, static_folder='static', template_folder='templates')

# Initialize detector
detector = DroneDetector()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/status')
def status():
    return jsonify(detector.get_status())

@app.route('/emergency', methods=['POST'])
def emergency():
    timestamp = datetime.now().strftime("%H:%M:%S")
    return jsonify({
        "status": "success",
        "message": f"Emergency alert at {timestamp}",
        "siren": True
    })

@app.route('/health')
def health():
    return 'OK', 200

@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == '__main__':
    # Start detection thread
    threading.Thread(target=detector.simulate_detection, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)