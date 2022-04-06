import subprocess


class Audio:
    
    def play_audio(self, file):
        
        process = subprocess.Popen(["play", file])
