import os
from .Camera import Camera
from .AudioGetter import AudioGetter
from .Audio import Audio
from .AudioStoring import AudioStoring
from .ProtocolReader import ProtocolReader
from .Micro import Micro
import subprocess
import time


class IntermediaryMode:

    def __init__(self, file):
        self.camera = Camera(file)
        self.volume = 100
        self.micro = Micro()
        self.audio = Audio()
        self.recording = False

    def getVolume(self):
        volumeFile = open("./database/sound-volume.txt", "r")
        volumeLine = volumeFile.readline()
        if isinstance(volumeLine, str):
            volumeFile.seek(0)
            if volumeLine != "":
                volumeFile.seek(0)
                self.volume = int(volumeLine)

    def action(self, button, patternSaved, pattern):
        protocol = ProtocolReader(button)
        protocol.decodeProtocol()
        sensor = protocol.sensor
        value = protocol.value
        self.getVolume()

        if sensor == "button18" and patternSaved:
            self.recButtonSend(value, pattern)
        if sensor == "button17":
            self.cameraButtonSend()
        if sensor == "button4" and patternSaved:
            self.delButtonSend(value, pattern)


    def recButtonSend(self, value, pattern):
        if value == "on":
            audioGet = AudioGetter(pattern)
            audioFile = audioGet.get_audio()
            if "noMessageRecorded" in audioFile:
                self.recording = True
                self.getVolume()
                self.audio.play_audio("audio/systemAudio/soundChanged.ogg", self.volume)
                self.micro.start_recording(pattern)
            else:
                self.getVolume()
                self.audio.play_audio("audio/systemAudio/soundChanged.ogg", self.volume)
        elif value == "off" and self.recording:
            self.micro.stop_recording()
            self.recording = False
            self.getVolume()
            self.audio.play_audio("audio/systemAudio/soundChanged.ogg", self.volume)

    def delButtonSend(self, value, pattern):
        audioGet = AudioGetter(pattern)
        audioFile = audioGet.get_audio()
        if "noMessageRecorded" in audioFile:
            self.getVolume()
            self.audio.play_audio("audio/systemAudio/soundChanged.ogg", self.volume)
        else:
            if value == "HIGH":
                audioDelete = AudioStoring("", pattern)
                audioDelete.deleteAudio()
            elif value == "1":
                self.audio.play_audio("audio/systemAudio/deleteConfirmationIntermediary.ogg", self.volume)

    def cameraButtonSend(self):
        led = subprocess.Popen(["python", "./led.py"])
        self.camera.take_photo()
        time.sleep(5)
        led.terminate()
        


""" intermediaryMode = IntermediaryMode("boo.png")
intermediaryMode.action("button17:on", False, 0)
intermediaryMode.action("button18:on", True, 1)
intermediaryMode.action("button18:off", True, 1)
 """