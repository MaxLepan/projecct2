from simple_websocket_server import WebSocketServer, WebSocket
from ProtocolReader import ProtocolReader

class SimpleEcho(WebSocket):
    
    def handle(self):
        print(self.data)
        protocol = ProtocolReader(self.data)
        sensor = protocol.sensor
        self.send_message(self.data)
        
    def connected(self):
        print(self.address, 'connected')
        
    def handle_close(self):
        print(self.address, 'closed')
        
        
server = WebSocketServer('', 8000, SimpleEcho)
server.serve_forever()

