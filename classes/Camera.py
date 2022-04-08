import subprocess
import time


class Camera:
    
    def __init__(self, name):
        self.process = subprocess.Popen(["echo", "Camera connecté"])
        self.name = name
    
    def take_photo(self):
        self.process = subprocess.Popen(["libcamera-still", "-t", "2000", "-o",self.name])