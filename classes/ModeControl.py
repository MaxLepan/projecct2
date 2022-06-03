from RPi import GPIO
from time import sleep
import os
import time
from datetime import datetime
from Audio import Audio


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
        self.lastMode = self.initMode()
        self.mode = self.initMode()
        self.audio = Audio()

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
        file = open(self.saveFilePath, "r")
        self.lastMode = int(file.readline())
        self.save()

        self.clkLastState = clkState
        sleep(0.01)

    def setSave(self):
        self.isSave = False
        self.lastChange = datetime.now()

    def initMode(self) -> int:
        file = open(self.saveFilePath, "r")
        return int(file.readline())
    
    def initCounter(self):
        file = open("./database/counter_mode.txt", "r")
        return int(file.readline())

    def save(self):
        delta = datetime.now() - self.lastChange
        if int(delta.total_seconds()) > 0.01 and self.isSave == False:
            print("Save")
            file = open(self.saveFilePath, "w")
            file.write(f"{self.mode}")
            fileCounter = open("./database/counter_mode.txt", "w")
            fileCounter.write(f"{self.counter}")
            self.isSave = True
            volumeFile = open("./database/sound-volume.txt", "r")
            volume = int(volumeFile.readline())
            soundFile = ""
            if self.lastMode != self.mode:
                if self.mode == 1:
                    soundFile = "start-mode-expert"
                elif self.mode == 2:
                    soundFile = "start-mode-intermediary"
                elif self.mode == 3:
                    soundFile = "start-mode-tutorial"
                self.audio.play_audio(f"audio/systemAudio/{soundFile}.ogg", volume)

            
modeControle = ModeControl("Mode")
modeControle.start()
