from simple_websocket_server import WebSocketServer, WebSocket
import os
from classes.Camera import Camera
from classes.ProtocolReader import ProtocolReader
from classes.Tensorflow import TensorFlow
import time


class Stockage:

    def __init__(self):
        self.temp = 0
        self.prox = 0,
        self.pattern = 0


class SimpleEcho(WebSocket):

    stockage = Stockage()
    camera = Camera("./img/photo_analyse.png")
    tensorflow = TensorFlow()
    
    def handle(self):
        protocol = ProtocolReader(self.data)
        protocol.decodeProtocol()
        sensor = protocol.sensor
        if sensor == "button17":
            SimpleEcho.camera.take_photo()
            time.sleep(2)
            SimpleEcho.tensorflow.get_pattern()
            print(SimpleEcho.tensorflow.pattern)
        elif sensor == "temp":
            SimpleEcho.stockage.temp = protocol.value
            print(protocol.value)
        elif sensor == "Proximity":
            SimpleEcho.stockage.prox = protocol.value
            print(protocol.value)
        elif sensor == "button18":
            print("18")
        elif sensor == "button4":
            print("4")
        
    def connected(self):
        print(self.address, 'connected')
        
    def handle_close(self):
        print(self.address, 'closed')
        
        
server = WebSocketServer('', 8000, SimpleEcho)
print("server online")
server.serve_forever()

