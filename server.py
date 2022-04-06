from simple_websocket_server import WebSocketServer, WebSocket
from ProtocolReader import ProtocolReader
import os


class Stockage:

    def __init__(self):
        self.temp = 0
        self.prox = 0


class SimpleEcho(WebSocket):

    stockage = Stockage()
    
    def handle(self):
        protocol = ProtocolReader(self.data)
        protocol.decodeProtocol()
        sensor = protocol.sensor
        if sensor == "button":
            if float(SimpleEcho.stockage.temp) > 25 and float(SimpleEcho.stockage.prox) > 190:
                print("Action a effectuer")
            else:
                print(SimpleEcho.stockage.temp, + SimpleEcho.stockage.prox)
                print("nope")
        elif sensor == "temp":
            SimpleEcho.stockage.temp = protocol.value
        elif sensor == "prox":
            SimpleEcho.stockage.prox = protocol.value
        #    os.system("raspistill -o Desktop/newimage.png")
        #self.send_message(self.data)
        
    def connected(self):
        print(self.address, 'connected')
        
    def handle_close(self):
        print(self.address, 'closed')
        
        
server = WebSocketServer('', 8000, SimpleEcho)
print("server online")
server.serve_forever()

