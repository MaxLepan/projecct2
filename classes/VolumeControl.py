from RPi import GPIO
from time import sleep
import alsaaudio
import os
from datetime import datetime


class VolumeControl:
    clk = 17
    dt = 18
    counter = 50
    mixer = alsaaudio.Mixer()
    isSave = True
    saveFilePath = "./database/sound-volume.txt"

    def __init__(self, name: str) -> None:
        self.name = name
        self.counter = self.initCounter()
        self.setupHardware()
        self.clkLastState = GPIO.input(self.clk)
        self.lastChange = datetime.now()
        self.lastValue = self.counter

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
                if self.counter < 100:
                    self.counter += 1
            else:
                if self.counter > 0:
                    self.counter -= 1
            self.mixer.setvolume(self.counter)
            print(self.mixer.getvolume())
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
        if int(delta.total_seconds()) > 1 and self.isSave == False:
            print("Save")
            file = open(self.saveFilePath, "w")
            file.write(f"{self.counter}")
            self.isSave = True
            os.system("play audio/systemAudio/soundChanged.ogg")

#Uncomment to run tests
#vs = VolumeControl("Volume")
#vs.start()
