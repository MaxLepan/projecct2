from simple_websocket_server import WebSocketServer, WebSocket
from classes.ProtocolReader import ProtocolReader
from classes.AudioGetter import AudioGetter
from classes.Audio import audio
from classes.Tutorial import Tutorial
from classes.ExpertMode import ExpertMode
from classes.IntermediaryMode import IntermediaryMode

clients = []

recMode = False 
tutoMode = Tutorial()
expertMode = ExpertMode("./img/photo_analyse.png")
intermediaryMode = IntermediaryMode("./img/photo_analyse.png")
audio = audio

class Stockage:

    def __init__(self):
        self.pattern = 0
        self.mode = 1
        self.volume = 100
        self.patternSaved = False

stockage = Stockage()

class SimpleEcho(WebSocket):
    global tutoMode
    global recMode
    global expertMode 
    global intermediaryMode
    global audio
    global stockage

    def handle(self):
        protocol = ProtocolReader(self.data)
        protocol.decodeProtocol()
        sensor = protocol.sensor
        value = protocol.value
        
        with open("./database/mode.txt", "r") as modeFile:
            modeLine = modeFile.readline()
            if isinstance(modeLine, str):
                if modeLine != "":
                    if stockage.mode != int(modeLine):
                        self.restartMode()
                    stockage.mode = int(modeLine)

        volumeFile = open("./database/sound-volume.txt", "r")
        volumeLine = volumeFile.readline()
        if isinstance(volumeLine, str):
            volumeFile.seek(0)
            if volumeLine != "":
                volumeFile.seek(0)
                stockage.volume = int(volumeLine)
        
        if sensor == "Tensorflow":
            stockage.pattern = value
            print(value)
            audioGetter = AudioGetter(value)
            audioFile = audioGetter.get_audio()
            print(audioFile)
            audio.play_audio(audioFile, stockage.volume+25)
            stockage.patternSaved = True


        elif stockage.mode == 1:
            expertMode.action(self.data, stockage.patternSaved, stockage.pattern)
            if sensor == "button17":
                for client in clients:
                    if client != self:
                        client.send_message("Tensorflow ready")

        elif stockage.mode == 2:
            intermediaryMode.action(self.data, stockage.patternSaved, stockage.pattern)
            if sensor == "button17":
                for client in clients:
                    if client != self:
                        client.send_message("Tensorflow ready")
        
        elif stockage.mode == 3:
            tutoMode.action(self.data)

    def connected(self):
        print(self.address, 'connected')
        clients.append(self)
        
    def handle_close(self):
        print(self.address, 'closed')
        clients.remove(self)
    
    def restartMode(self):
        tutoMode.cameraButton = False
        tutoMode.recButton = False
        tutoMode.delButton = False
        stockage.patternSaved = False
        
        
server = WebSocketServer('', 8080, SimpleEcho)
print("server online")
server.serve_forever()
