from simple_websocket_server import WebSocketServer, WebSocket
import os
from classes.Camera import Camera
from classes.ProtocolReader import ProtocolReader
from classes.Tensorflow import TensorFlow
from classes.AudioGetter import AudioGetter
from classes.Audio import Audio
from classes.AudioStoring import AudioStoring
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
    audio = Audio()
    
    def handle(self):
        protocol = ProtocolReader(self.data)
        protocol.decodeProtocol()
        sensor = protocol.sensor
        # Takes photo
        if sensor == "button17":
            
            # Scan pattern
            SimpleEcho.camera.take_photo()
            time.sleep(2)
            SimpleEcho.tensorflow.get_pattern()
            SimpleEcho.stockage.pattern = SimpleEcho.tensorflow.pattern
            
            # Plays audio at scan
            audioGetter = AudioGetter(SimpleEcho.stockage.pattern)
            print(audioGetter.get_audio())
            audioFile = audioGetter.get_audio()
            SimpleEcho.audio.play_audio(audioFile)
            
            print(SimpleEcho.tensorflow.pattern)
        elif sensor == "temp":
            SimpleEcho.stockage.temp = protocol.value
            print(protocol.value)
        elif sensor == "Proximity":
            SimpleEcho.stockage.prox = protocol.value
            print(protocol.value)
        elif sensor == "button18":
            print("18")
            self.send_message(str(SimpleEcho.stockage.pattern))
            
        elif sensor == "button4":
            # audioGetter = AudioGetter(SimpleEcho.stockage.pattern)
            # print(audioGetter.get_audio())
            # audioFile = audioGetter.get_audio()
            # SimpleEcho.audio.play_audio(audioFile)
            audioDelete = AudioStoring("", SimpleEcho.stockage.pattern)
            audioDelete.deleteAudio()
            
            print("button4")
        
    def connected(self):
        print(self.address, 'connected')
        
    def handle_close(self):
        print(self.address, 'closed')
        
        
server = WebSocketServer('', 8000, SimpleEcho)
print("server online")
server.serve_forever()

# button = subprocess.Popen(["python", "bouton.py"])
# print("All online")