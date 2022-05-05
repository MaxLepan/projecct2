from .Audio import Audio

class ButtonDelete:
    volume = 100

    def __init__(self):
        self.audio = Audio()

    def mode_1(self):
        print("del accompagner")
    
    def mode_2(self):
        self.audio.play_audio("./audio/systemAudio/start-mode-2")
    
    def mode_3(self):
        self.audio.play_audio("./audio/systemAudio/start-mode-3")

    def action(self, mode):
        file = open("./database/sound-volume.txt", "r")
        ButtonDelete.volume = int(file.readline())
        if mode == 1:
            self.mode_1()
        elif mode == 2:
            self.mode_2()
        elif mode == 3:
            self.mode_3()