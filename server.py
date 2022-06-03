from simple_websocket_server import WebSocketServer, WebSocket
from classes.ProtocolReader import ProtocolReader
from classes.AudioGetter import AudioGetter
from classes.Audio import Audio
from classes.Tutorial import Tutorial
from classes.ExpertMode import ExpertMode
from classes.IntermediaryMode import IntermediaryMode

clients = []




class Stockage:

    def __init__(self):
        self.pattern = 0
        self.mode = 1
        self.volume = 100



class SimpleEcho(WebSocket):
    #global tutoMode
    #global patternSaved
    #global recMode
    #global expertMode 
    #global intermediaryMode
    #global audio
    #global stockage
    patternSaved = False
    recMode = False 
    tutoMode = Tutorial()
    expertMode = ExpertMode("./img/photo_analyse.png")
    intermediaryMode = IntermediaryMode("./img/photo_analyse.png")
    audio = Audio()
    stockage = Stockage()

    def handle(self):
        protocol = ProtocolReader(self.data)
        protocol.decodeProtocol()
        sensor = protocol.sensor
        value = protocol.value
        
        with open("./database/mode.txt", "r") as modeFile:
            modeLine = modeFile.readline()
            if isinstance(modeLine, str):
                if modeLine != "":
                    if SimpleEcho.stockage.mode != int(modeLine):
                        self.restartMode()
                    SimpleEcho.stockage.mode = int(modeLine)
        volumeFile = open("./database/sound-volume.txt", "r")
        volumeLine = volumeFile.readline()
        if isinstance(volumeLine, str):
            volumeFile.seek(0)
            if volumeLine != "":
                volumeFile.seek(0)
                SimpleEcho.stockage.volume = int(volumeLine)
        
        if sensor == "Tensorflow":
            SimpleEcho.stockage.pattern = value
            print(value)
            audioGetter = AudioGetter(value)
            audioFile = audioGetter.get_audio()
            print(audioFile)
            SimpleEcho.audio.play_audio(audioFile, SimpleEcho.stockage.volume)
            SimpleEcho.patternSaved = True


        elif SimpleEcho.stockage.mode == 1:
            print("In simple Mode 1")
            SimpleEcho.expertMode.action(self.data, SimpleEcho.patternSaved, SimpleEcho.stockage.pattern)
            if sensor == "button17":
                for client in clients:
                    if client != self:    
                        client.send_message("Tensorflow ready")

        elif SimpleEcho.stockage.mode == 2:
            SimpleEcho.intermediaryMode.action(self.data, SimpleEcho.patternSaved, SimpleEcho.stockage.pattern)
            if sensor == "button17":
                for client in clients:
                    if client != self:
                        client.send_message("Tensorflow ready")
        
        elif SimpleEcho.stockage.mode == 3:
            if sensor == "button18" and value == "on":
                SimpleEcho.tutoMode.action(sensor)
            elif sensor != "button18":
                SimpleEcho.tutoMode.action(sensor)

    def connected(self):
        print(self.address, 'connected')
        clients.append(self)
        
    def handle_close(self):
        print(self.address, 'closed')
        clients.remove(self)
    
    def restartMode(self):
        SimpleEcho.tutoMode.cameraButton = False
        SimpleEcho.tutoMode.recButton = False
        SimpleEcho.tutoMode.delButton = False
        SimpleEcho.patternSaved = False
        
        
server = WebSocketServer('', 8080, SimpleEcho)
print("server online")
server.serve_forever()
