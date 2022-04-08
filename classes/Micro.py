import subprocess
from datetime import datetime
from AudioStoring import AudioStoring
import time
import json


class Micro:
    
    def __init__(self):
        self.process = subprocess.Popen(["echo", "Micro connecté"])
        self.file = "audio/audioFiles/audio_"+str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))+".ogg"
    
    def start_recording(self):
        self.process = subprocess.Popen(["rec", self.file])
        with open("./audio/audioStorage.json") as file:
            audioFile = json.load(file)

        audio_storing = AudioStoring(self.file, len(audioFile["audioFiles"])+1)
        audio_storing.store()
        
    def stop_recording(self):
        self.process.terminate()
        

# Uncomment to run tests
micro = Micro()
micro.start_recording()
time.sleep(2)
micro.stop_recording()
