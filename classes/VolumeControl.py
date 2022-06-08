from RPi import GPIO
from time import sleep
import os
from datetime import datetime
from Audio import Audio


class VolumeControl:
    clk = 24
    dt = 23
    counter = 50
    isSave = True
    saveFilePath = "./database/sound-volume.txt"

    def __init__(self, name: str) -> None:
        self.name = name
        self.counter = self.initCounter()
        self.setupHardware()
        self.clkLastState = GPIO.input(self.clk)
        self.lastChange = datetime.now()
        self.lastValue = self.counter
        self.audio = Audio()

    def start(self):
        print(self.name, " is working !")
        try:
            while True:
                self.changeVolume()
        finally:
            GPIO.cleanup()

    def setupHardware(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def changeVolume(self):
        clkState = GPIO.input(self.clk)
        dtState = GPIO.input(self.dt)
        if clkState != self.clkLastState:
            if dtState != clkState:
                if self.counter < 150:
                    self.counter += 1
            else:
                if self.counter > 1:
                    self.counter -= 1
            print(self.counter)
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
            file = open(self.saveFilePath, "w")
            file.write(f"{self.counter}")
            self.isSave = True
            
            self.audio.play_audio("audio/systemAudio/soundChanged.ogg", self.counter)

#Uncomment to run tests
vs = VolumeControl("Volume")
vs.start()
