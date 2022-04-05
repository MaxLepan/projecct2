import RPi.GPIO as GPIO
import dht11
from ProtocolBuilder import ProtocolBuilder
import websocket

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

instance = dht11.DHT11(pin = 14)
ws = websocket.create_connection("ws://localhost:8000")

try:
    while True:
        result = instance.read()
        if result.is_valid():
            tempProtocol = ProtocolBuilder("temp", result.temperature)
            humidityProtocol = ProtocolBuilder("humidity", result.humidity)
            ws.send(tempProtocol.buildProtocol())
            ws.send(humidityProtocol.buildProtocol())
except KeyboardInterrupt:
    GPIO.cleanup()
    print("quit the loop")