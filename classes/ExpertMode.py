import os
from .Camera import Camera
from .ProtocolReader import ProtocolReader
import subprocess
import time

class ExpertMode:

    def __init__(self, file):
        self.camera = Camera(file)
        self.volume = 100

    def action(self, button):
        protocol = ProtocolReader(button)
        protocol.decodeProtocol()
        sensor = protocol.sensor
        value = protocol.value
        volumeFile = open("./database/sound-volume.txt", "r")
        volumeLine = volumeFile.readline()
        if isinstance(volumeLine, str):
            volumeFile.seek(0)
            if volumeLine != "":
                volumeFile.seek(0)
                self.volume = int(volumeLine)
        if sensor == "button18" and value != "off":
            self.recButtonSend()
        if sensor == "button17":
            self.cameraButtonSend()
        if sensor == "button4":
            self.delButtonSend()


    def recButtonSend(self):
        print("boo")

    def delButtonSend(self):
        print("boo del")

    def cameraButtonSend(self):
        print("ici")
        led = subprocess.Popen(["python", "./led.py"])
        self.camera.take_photo()
        time.sleep(2)
        led.terminate()
        


#expertMode = ExpertMode("boo.png")
#expertMode.action("button17:on")