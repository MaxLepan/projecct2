from .Audio import Audio
from .AudioStoring import AudioStoring

class ButtonDelete:
    volume = 100

    def __init__(self):
        self.audio = Audio()

    def mode_1(self, pattern):
        print("del accompagner")
        audioDelete = AudioStoring("", pattern)
        audioDelete.deleteAudio()
    
    def mode_2(self, pattern):
        self.audio.play_audio("audio/systemAudio/start-mode-2.ogg", ButtonDelete.volume)
        audioDelete = AudioStoring("", pattern)
        audioDelete.deleteAudio()
    
    def mode_3(self, pattern):
        self.audio.play_audio("audio/systemAudio/start-mode-3.ogg", ButtonDelete.volume)
        audioDelete = AudioStoring("", pattern)
        audioDelete.deleteAudio()

    def action(self, mode, pattern):
        file = open("./database/sound-volume.txt", "r")
        ButtonDelete.volume = int(file.readline())
        if mode == 1:
            self.mode_1(pattern)
        elif mode == 2:
            self.mode_2(pattern)
        elif mode == 3:
            self.mode_3(pattern)