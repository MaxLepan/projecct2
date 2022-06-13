from .Camera import Camera
from .AudioGetter import AudioGetter
from .Audio import audio
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
        self.audio = audio
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
                self.audio.play_audio("audio/systemAudio/start-enregistrement.ogg", self.volume)
                self.micro.start_recording(pattern)
            else:
                self.getVolume()
                self.audio.play_audio("audio/systemAudio/refus.ogg", self.volume)
                time.sleep(0.5)
                self.audio.play_audio("audio/systemAudio/messageAlreadyRecorded.ogg", self.volume)
        elif value == "off" and self.recording:
            self.micro.stop_recording()
            self.recording = False
            time.sleep(0.5)
            self.getVolume()
            self.audio.play_audio("audio/systemAudio/validation.ogg", self.volume)
            time.sleep(0.5)
            self.audio.play_audio("audio/systemAudio/messageRecorded.ogg", self.volume)

    def delButtonSend(self, value, pattern):
        audioGet = AudioGetter(pattern)
        audioFile = audioGet.get_audio()
        if "noMessageRecorded" in audioFile:
            self.getVolume()
            self.audio.play_audio("audio/systemAudio/refus.ogg", self.volume)
            time.sleep(0.7)
            self.audio.play_audio("audio/systemAudio/nothingToDelete.ogg", self.volume)
        else:
            if value == "HIGH":
                audioDelete = AudioStoring("", pattern)
                audioDelete.deleteAudio()
                time.sleep(0.5)
                self.audio.play_audio("audio/systemAudio/messageDeleted.ogg", self.volume)
            elif value == "1":
                self.audio.play_audio("audio/systemAudio/deleteConfirmationIntermediary.ogg", self.volume)

    def cameraButtonSend(self):
        led = subprocess.Popen(["python", "./led.py"])
        audio.play_audio("audio/systemAudio/radard.ogg", self.volume)
        self.camera.take_photo()
        time.sleep(5)
        im = Image.open("./img/photo_analyse.jpg")
        w,h= im.size
        cropped = im.crop((1000, 700, w/2+200, h/2+300))
        cropped.save("./img/photo_analyse.jpg", "JPEG")
        led.terminate()
        

""" intermediaryMode = IntermediaryMode("boo.png")
intermediaryMode.action("button17:on", False, 0)
intermediaryMode.action("button18:on", True, 1)
intermediaryMode.action("button18:off", True, 1) """
