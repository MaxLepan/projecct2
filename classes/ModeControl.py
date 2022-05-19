from RPi import GPIO
from time import sleep
import os
from datetime import datetime

# Mode false is intermediary mode, true is expert mode

class ModeControl:
    pushpin = 12
    mode = False
    modeName = "intermediary"
    isSave = True
    saveFilePath = "./database/mode.txt"

    def __init__(self, name: str) -> None:
        self.name = name
        self.setupHardware()
        self.pushPinLastState = GPIO.input(self.pushpin)
        self.lastValue = self.mode

    def start(self):
        print(self.name, " is working !")
        try:
            while True:
                self.changeMode()
        finally:
            GPIO.cleanup()

    def setupHardware(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pushpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def changeMode(self):
        pushPinState = GPIO.input(self.pushpin)
        
        if pushPinState:
            self.mode = True
            self.modeName = "expert"
        else:
            self.mode = False 
            self.modeName = "intermediary"
        print(self.modeName)

        self.isSave = False
        self.save()

        self.pinPinLastState = pushPinState
        sleep(0.2)


    def save(self):
        if self.isSave == False:
            print("Save")
            file = open(self.saveFilePath, "w")
            file.write(f"{self.mode}")
            self.isSave = True
            volumeFile = open("./database/sound-volume.txt", "r")
            volume = int(volumeFile.readline())
            os.system(f"play -v {volume/100} ./audio/systemAudio/start-mode-{self.modeName}.ogg")
            
mode = ModeControl("mode")
mode.start()