from RPi import GPIO
from time import sleep
import os
from datetime import datetime


class ModeControl:
    clk = 16
    dt = 12
    counter = 50
    isSave = True
    saveFilePath = "./database/mode.txt"

    def __init__(self, name: str) -> None:
        self.name = name
        self.counter = self.initCounter()
        self.setupHardware()
        self.clkLastState = GPIO.input(self.clk)
        self.lastChange = datetime.now()
        self.lastValue = self.counter
        self.mode = 0

    def start(self):
        print(self.name, " is working !")
        try:
            while True:
                self.changeMode()
        finally:
            GPIO.cleanup()

    def setupHardware(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def changeMode(self):
        clkState = GPIO.input(self.clk)
        dtState = GPIO.input(self.dt)
        if clkState != self.clkLastState:
            if dtState != clkState:
                if self.counter < 15:
                    self.counter += 1
            else:
                if self.counter > 1:
                    self.counter -= 1
            if self.counter < 5:
                self.mode = 1
            elif self.counter > 5 and self.counter < 10:
                self.mode = 2
            elif self.counter > 10:
                self.mode = 3
            
            print(self.counter, "MODE", self.mode)
            self.setSave()

        self.save()

        self.clkLastState = clkState
        sleep(0.01)

    def setSave(self):
        self.isSave = False
        self.lastChange = datetime.now()

    def initCounter(self) -> int:
        file = open(self.saveFilePath, "r")
        return int(file.readline())

    def save(self):
        delta = datetime.now() - self.lastChange
        if int(delta.total_seconds()) > 0.01 and self.isSave == False:
            print("Save")
            lastModeFile = open(self.saveFilePath, "r")
            lastMode = int(lastModeFile.readline())
            file = open(self.saveFilePath, "w")
            file.write(f"{self.mode}")
            self.isSave = True
            volumeFile = open("./database/sound-volume.txt", "r")
            volume = int(volumeFile.readline())
            soundFile = ""
            if lastMode != self.mode:
                if self.mode == 1:
                    soundFile = "start-mode-expert"
                elif self.mode == 2:
                    soundFile = "start-mode-intermediary"
                elif self.mode == 3:
                    soundFile = "button-camera-tuto"
                    os.system(f"play -v {volume/100} audio/systemAudio/start-mode-tutoriel-1.ogg")
                    os.system(f"play -v {volume/100} audio/systemAudio/start-mode-tutoriel-2.ogg")
                os.system(f"play -v {volume/100} audio/systemAudio/{soundFile}.ogg")

            
modeControle = ModeControl("Mode")
modeControle.start()
