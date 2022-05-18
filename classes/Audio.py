import subprocess


class Audio:
    
    def play_audio(self, file, volume):
        
        process = subprocess.Popen(["play", "-v", str(volume/100), file])

#audio = Audio()
#audio.play_audio("../audio/audioFiles/test.ogg")