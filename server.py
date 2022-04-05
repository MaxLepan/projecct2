from simple_websocket_server import WebSocketServer, WebSocket
from ProtocolReader import ProtocolReader
import os

class SimpleEcho(WebSocket):
    
    def handle(self):
        print(self.data)
        protocol = ProtocolReader(self.data)
        protocol.decodeProtocol()
        sensor = protocol.sensor
        print(sensor)
        if (sensor == "button"):
            os.system("raspistill -o Desktop/newimage.png")
        #self.send_message(self.data)
        
    def connected(self):
        print(self.address, 'connected')
        
    def handle_close(self):
        print(self.address, 'closed')
        
        
server = WebSocketServer('', 8000, SimpleEcho)
print("server online")
server.serve_forever()

