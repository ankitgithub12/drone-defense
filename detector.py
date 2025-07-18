import time
import random
import math
import threading
from datetime import datetime

class DroneDetector:
    def __init__(self):
        self.detected = False
        self.location = (28.6139, 77.2090)
        self.distance = 0
        self.last_detection = None
        self.nodes = [
            {"id": 1, "lat": 28.6139, "lon": 77.2090, "last_rssi": -90},
            {"id": 2, "lat": 28.6145, "lon": 77.2102, "last_rssi": -90},
            {"id": 3, "lat": 28.6122, "lon": 77.2078, "last_rssi": -90}
        ]
        self._status_cache = None
        self._cache_lock = threading.Lock()
        self._cache_timeout = 1  # seconds

    def simulate_detection(self):
        while True:
            if random.random() < 0.3:  # 30% detection chance
                self.detected = True
                self.last_detection = datetime.now().strftime("%H:%M:%S")
                
                angle = random.uniform(0, 2*math.pi)
                self.distance = random.randint(50, 800)
                offset = self.distance * 0.00001
                self.location = (
                    28.6139 + offset * math.cos(angle),
                    77.2090 + offset * math.sin(angle)
                )
                
                for node in self.nodes:
                    dist = 1000 * math.sqrt(
                        (node['lat']-self.location[0])**2 + 
                        (node['lon']-self.location[1])**2
                    )
                    node['last_rssi'] = max(-90, -40 - int(dist/20))
                
                print(f"🚨 Drone detected! {self.distance}m away")
            else:
                self.detected = False
            
            time.sleep(10)  # Check every 10 seconds

    def get_status(self):
        with self._cache_lock:
            current_time = time.time()
            if (not self._status_cache or 
                current_time - self._status_cache['timestamp'] > self._cache_timeout):
                self._status_cache = {
                    "detected": self.detected,
                    "location": self.location,
                    "distance": self.distance,
                    "time": self.last_detection,
                    "nodes": self.nodes,
                    "timestamp": current_time
                }
            return self._status_cache.copy()