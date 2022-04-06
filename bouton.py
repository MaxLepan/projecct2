import time
import websocket
import RPi.GPIO as GPIO
from ProtocolBuilder import ProtocolBuilder
from micro import Micro
from audio import Audio

GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
print(GPIO.input(17))
ws = websocket.create_connection("ws://localhost:8000")

micro = Micro()
audio = Audio()


while True:
    
    if GPIO.input(17) == GPIO.HIGH:
        print("pushed")
        protocol = ProtocolBuilder("button17", "HIGH")
        ws.send(protocol.buildProtocol())
        time.sleep(2)
    if GPIO.input(18) == GPIO.HIGH:
        micro.start_recording()
        while GPIO.input(18) == GPIO.HIGH:
            time.sleep(0.1)
    if GPIO.input(18) == GPIO.LOW:
        micro.stop_recording()
    if GPIO.input(4) == GPIO.HIGH:
        audio.play_audio("audio/test.ogg")
        print("pushed")
        protocol = ProtocolBuilder("button4", "HIGH")
        ws.send(protocol.buildProtocol())
        time.sleep(2)
    