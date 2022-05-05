import time
import websocket
import os
import RPi.GPIO as GPIO
from classes.ProtocolBuilder import ProtocolBuilder
from classes.Micro import Micro
from classes.Audio import Audio
from datetime import datetime
from classes.ButtonRec import ButtonRec

GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
print(GPIO.input(17))
ws = websocket.create_connection("ws://localhost:8080")

micro = Micro()
audio = Audio()
buttonRec = ButtonRec()
DelMode = False
deleteTime = datetime.now()
saveMode = False

while True:
    time_now = datetime.now() - deleteTime
    if int(time_now.total_seconds()) > 5:
        DelMode = False
    # Takes photo
    if GPIO.input(17) == GPIO.HIGH:
        print("pushed")
        protocol = ProtocolBuilder("button17", "HIGH")
        ws.send(protocol.buildProtocol())
        time.sleep(2)

    # Start audio recording
    if GPIO.input(18) == GPIO.HIGH:
        protocol = ProtocolBuilder("button18", "on")
        ws.send(protocol.buildProtocol())
        pattern = ws.recv()
        saveMode = True
        while GPIO.input(18) == GPIO.HIGH:
            time.sleep(0.1)

    # Stops audio recording
    if GPIO.input(18) == GPIO.LOW:
        if saveMode:
            protocol = ProtocolBuilder("button18", "off")
            ws.send(protocol.buildProtocol())
            saveMode = False

    # Delete audio file
    if GPIO.input(4) == GPIO.HIGH:
        print(DelMode)
        if DelMode:
            print("pushed")
            protocol = ProtocolBuilder("button4", "HIGH")
            ws.send(protocol.buildProtocol())
            time.sleep(2)
            DelMode = False
        else:
            volumeFile = open("./database/sound-volume.txt", "r")
            volume = int(volumeFile.readline())
            os.system(f"play -v {volume/100} audio/systemAudio/soundChanged.ogg")
            DelMode = True
            deleteTime = datetime.now()
    