import subprocess


class Audio:
    
    def play_audio(self, file):
        
        process = subprocess.Popen(["play", file])

#audio = Audio()
#audio.play_audio("../audio/audioFiles/test.ogg")