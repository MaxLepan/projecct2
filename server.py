from simple_websocket_server import WebSocketServer, WebSocket
import os
from classes.Camera import Camera
from classes.ProtocolReader import ProtocolReader


class Stockage:

    def __init__(self):
        self.temp = 0
        self.prox = 0


class SimpleEcho(WebSocket):

    stockage = Stockage()
    camera = Camera("./img/photo_analyse.png")
    
    def handle(self):
        protocol = ProtocolReader(self.data)
        protocol.decodeProtocol()
        sensor = protocol.sensor
        if sensor == "button17":
            if float(SimpleEcho.stockage.temp) > 25 and float(SimpleEcho.stockage.prox) > 190:
                print("Action a effectuer")
            else:
                print(SimpleEcho.stockage.temp, SimpleEcho.stockage.prox)
                print("nope")
            SimpleEcho.camera.take_photo()
        elif sensor == "temp":
            SimpleEcho.stockage.temp = protocol.value
        elif sensor == "Proximity":
            SimpleEcho.stockage.prox = protocol.value
        elif sensor == "button18":
            print("18")
        elif sensor == "button4":
            print("4")
        #    os.system("raspistill -o Desktop/newimage.png")
        #self.send_message(self.data)
        
    def connected(self):
        print(self.address, 'connected')
        
    def handle_close(self):
        print(self.address, 'closed')
        
        
server = WebSocketServer('', 8000, SimpleEcho)
print("server online")
server.serve_forever()

