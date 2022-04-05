import time
import websocket
import RPi.GPIO as GPIO
from ProtocolBuilder import ProtocolBuilder

GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

ws = websocket.create_connection("ws://localhost:8000")

while True:
    if GPIO.input(17) == GPIO.HIGH:
        print("pushed")
        protocol = ProtocolBuilder("button", "HIGH")
        ws.send(protocol.buildProtocol())
        
        time.sleep(2)

