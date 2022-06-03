import os

from .Audio import Audio
from .Micro import Micro
from .ProtocolReader import ProtocolReader
from .AudioStoring import AudioStoring
from .AudioGetter import AudioGetter


class Tutorial:

    def __init__(self):
        self.cameraButton = False
        self.recButton = False
        self.delButton = False
        self.volume = 100
        self.micro = Micro()
        self.audio = Audio()

    def action(self, button):
        volumeFile = open("./database/sound-volume.txt", "r")
        volumeLine = volumeFile.readline()
        if isinstance(volumeLine, str):
            volumeFile.seek(0)
            if volumeLine != "":
                volumeFile.seek(0)
                self.volume = int(volumeLine)
        protocol = ProtocolReader(button)
        protocol.decodeProtocol()
        sensor = protocol.sensor
        value = protocol.value
        if not self.cameraButton or self.recButton == False or self.delButton == False:
            if sensor == "button18":
                self.recButtonSend(value)
            if sensor == "button17":
                self.cameraButtonSend()
            if sensor == "button4":
                self.delButtonSend(value)
        else:
            os.system(f"play -v {self.volume / 100} ./audio/systemAudio/fin-tutoriel.ogg")


    def recButtonSend(self, value):
        if self.recButton:
            os.system(f"play -v {self.volume / 100} ./audio/systemAudio/not-good-button.ogg")
        elif not self.cameraButton:
            os.system(f"play -v {self.volume / 100} ./audio/systemAudio/not-good-button.ogg")
        elif value == "on":
            self.audio.play_audio("audio/systemAudio/soundChanged.ogg", self.volume)
            self.micro.start_recording("tuto")
        elif value == "off":
            self.micro.stop_recording()
            os.system(f"play -v {self.volume / 100} ./audio/systemAudio/button-del-tuto.ogg")
            self.recButton = True


    def delButtonSend(self, value):
        if self.delButton:
            os.system(f"play -v {self.volume / 100} ./audio/systemAudio/not-good-button.ogg")
        elif not self.recButton or not self.cameraButton:
            os.system(f"play -v {self.volume / 100} ./audio/systemAudio/not-good-button.ogg")
        elif value == "HIGH":
            self.delButton = True
            audioDelete = AudioStoring("", "tuto")
            audioDelete.deleteAudio()
            os.system(f"play -v {self.volume / 100} ./audio/systemAudio/fin-tutoriel.ogg")
        elif value == "1":
            self.audio.play_audio("audio/systemAudio/deleteConfirmationIntermediary.ogg", self.volume)

    def cameraButtonSend(self):
        if self.cameraButton and self.recButton:
            audioGet = AudioGetter("tuto")
            audioFile = audioGet.get_audio()
            self.audio.play_audio(audioFile, self.volume)
        elif self.cameraButton and not self.recButton:
            self.audio.play_audio("audio/systemAudio/not-good-button.ogg", self.volume)
        else:
            self.cameraButton = True
            os.system(f"play -v {self.volume / 100} ./audio/systemAudio/button-rec-tuto.ogg")
            


#tutorial = Tutorial()
#tutorial.action("button18")
