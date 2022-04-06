import subprocess
from datetime import datetime

class Micro:
    
    def __init__(self):
        self.process = subprocess.Popen(["echo", "Micro connecté"])
    
    def start_recording(self):
        self.process = subprocess.Popen(["rec", "audio/test"+str(datetime.now())+".ogg"])
        
    def stop_recording(self):
        self.process.terminate()
        
        
