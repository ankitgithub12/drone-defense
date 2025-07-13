from flask import Flask, render_template, jsonify
from detector import DroneDetector
import threading
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__, static_folder='static', template_folder='templates')

# Initialize detector
detector = DroneDetector()

# Health check endpoint
@app.route('/health')
def health():
    return 'OK', 200

@app.route('/status')
def status():
    try:
        return jsonify(detector.get_status())
    except Exception as e:
        print(f"Status error: {str(e)}")
        return jsonify({"error": "Server error"}), 500

# Start detection thread
def run_detector():
    detector.simulate_detection()

threading.Thread(target=run_detector, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)