#import time
import subprocess


class Audio:
    def __init__(self) -> None:
        self.process = subprocess.Popen(["echo", "Audio"])
    
    def play_audio(self, file, volume):
        if self.process.poll() is None:
            self.process.terminate()
        self.process = subprocess.Popen(["play", "-v", str(volume/100), file])
"""
audio = Audio()
audio.play_audio("../audio/systemAudio/not-good-button.ogg",5)
time.sleep(0.5)
audio.play_audio("../audio/systemAudio/not-good-button.ogg",5)
time.sleep(3)
audio.play_audio("../audio/systemAudio/not-good-button.ogg",5)
"""