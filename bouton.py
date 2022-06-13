import time
import websocket
from classes.Audio import audio
import RPi.GPIO as GPIO
from classes.ProtocolBuilder import ProtocolBuilder
from datetime import datetime

GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
ws = websocket.create_connection("ws://localhost:8080")
audio = audio

DelMode = False
deleteTime = datetime.now()
saveMode = False
recTime = datetime.now()
canStart = True
isRecording = False
photoTime = datetime.now()
camActive = False
buttonCPressed = False

button18Pressed = False
button4Pressed = False

while True:
    volume = 100
    volumeFile = open("./database/sound-volume.txt", "r")
    volumeLine = volumeFile.readline()
    if isinstance(volumeLine, str):
            if volumeLine != "":
                volumeFile.seek(0)
                volume = int(volumeLine)
    time_now = datetime.now() - deleteTime
    if int(time_now.total_seconds()) > 7:
        DelMode = False
    photoTime_now = datetime.now() - photoTime
    if int(photoTime_now.total_seconds()) > 12:
        camActive = False
    # Takes photo
    if GPIO.input(17) == GPIO.HIGH:
        if buttonCPressed == False:
            buttonCPressed = True

    if GPIO.input(17) == GPIO.LOW:
         if buttonCPressed == True:
            buttonCPressed = False
            if camActive == False:
                protocol = ProtocolBuilder("button17", "HIGH")
                ws.send(protocol.buildProtocol())
                time.sleep(2)
                camActive = True
                photoTime = datetime.now()
                time.sleep(1)

    # Start audio recording

    if GPIO.input(18) == GPIO.HIGH:

        if button18Pressed == False:
            button18Pressed = True
            recTime = datetime.now()
        else:
            delta = datetime.now() - recTime
            if int(delta.total_seconds()) > 1.0:
                if canStart:
                    canStart = False
                    print("Declenche enregistrement")
                    protocol = ProtocolBuilder("button18", "on")
                    ws.send(protocol.buildProtocol())

    # Stops audio recording
    if GPIO.input(18) == GPIO.LOW:

        if button18Pressed == True:
            button18Pressed = False
            delta = datetime.now() - recTime
            if int(delta.total_seconds()) < 0.20:
                print("Appuie court")
                audio.play_audio("audio/systemAudio/keepPushingToRecord.ogg", volume)
            else:
                print("Fin de l'enregistrement")
                canStart = True
                protocol = ProtocolBuilder("button18", "off")
                ws.send(protocol.buildProtocol())

        time.sleep(0.2)

    # Delete audio file
    if GPIO.input(4) == GPIO.HIGH:
        print('boo')
        if button4Pressed == False:
            button4Pressed = True

    if GPIO.input(4) == GPIO.LOW:
         if button4Pressed == True:
            button4Pressed = False
            if DelMode:
                protocol = ProtocolBuilder("button4", "HIGH")
                ws.send(protocol.buildProtocol())
                time.sleep(2)
                DelMode = False
            else:
                protocol = ProtocolBuilder("button4", "1")
                ws.send(protocol.buildProtocol())
                DelMode = True
                deleteTime = datetime.now()
                time.sleep(0.2)

    time.sleep(0.2)
