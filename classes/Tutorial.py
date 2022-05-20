import os

class Tutorial:

    def __init__(self):
        self.cameraButton = False
        self.recButton = False
        self.delButton = False
        self.volume = 100

    def action(self, button):
        volumeFile = open("./database/sound-volume.txt", "r")
        volumeLine = volumeFile.readline()
        if isinstance(volumeLine, str):
            volumeFile.seek(0)
            if volumeLine != "":
                volumeFile.seek(0)
                self.volume = int(volumeLine)
        if not self.cameraButton or self.recButton == False or self.delButton == False:
            if button == "button18":
                self.recButtonSend()
            if button == "button17":
                self.cameraButtonSend()
            if button == "button4":
                self.delButtonSend()
        else:
            os.system(f"play -v {self.volume / 100} ./audio/systemAudio/fin-tutoriel.ogg")


    def recButtonSend(self):
        if self.recButton:
            os.system(f"play -v {self.volume / 100} ./audio/systemAudio/not-good-button.ogg")
        elif not self.cameraButton:
            os.system(f"play -v {self.volume / 100} ./audio/systemAudio/not-good-button.ogg")
        else:
            self.recButton = True
            os.system(f"play -v {self.volume / 100} ./audio/systemAudio/button-del-tuto.ogg")

    def delButtonSend(self):
        if self.delButton:
            os.system(f"play -v {self.volume / 100} ./audio/systemAudio/not-good-button.ogg")
        elif not self.recButton or not self.cameraButton:
            os.system(f"play -v {self.volume / 100} ./audio/systemAudio/not-good-button.ogg")
        else:
            self.delButton = True
            os.system(f"play -v {self.volume / 100} ./audio/systemAudio/fin-tutoriel.ogg")

    def cameraButtonSend(self):
        if self.cameraButton:
            os.system(f"play -v {self.volume / 100} ./audio/systemAudio/not-good-button.ogg")
        else:
            self.cameraButton = True
            os.system(f"play -v {self.volume / 100} ./audio/systemAudio/button-rec-tuto.ogg")
            


#tutorial = Tutorial()
#tutorial.action("button18")
