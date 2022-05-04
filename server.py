from simple_websocket_server import WebSocketServer, WebSocket
from classes.Camera import Camera
from classes.ProtocolReader import ProtocolReader
from classes.Tensorflow import TensorFlow
from classes.Audio import Audio
from classes.AudioStoring import AudioStoring
from classes.ButtonRec import ButtonRec
from classes.ButtonDelete import ButtonDelete
from classes.ButtonCamera import ButtonCamera
from classes.VolumeControl import VolumeControl


class Stockage:

    def __init__(self):
        self.pattern = 0
        self.mode = 1


class SimpleEcho(WebSocket):

    stockage = Stockage()
    camera = Camera("./img/photo_analyse.png")
    tensorflow = TensorFlow()
    audio = Audio()
    buttonRec = ButtonRec()
    buttonDelete = ButtonDelete()
    buttonCamera = ButtonCamera("./img/photo_analyse.png")
    volumeControl = VolumeControl("Volume")
    
    def handle(self):
        protocol = ProtocolReader(self.data)
        protocol.decodeProtocol()
        sensor = protocol.sensor
        # Takes photo
        if sensor == "button17":
            SimpleEcho.stockage.pattern = SimpleEcho.buttonCamera.action(SimpleEcho.stockage.mode)
            
            # Scan pattern
            """ led = subprocess.Popen(["python", "./led.py"])
            SimpleEcho.camera.take_photo()
            time.sleep(2)
            print("photo")
            SimpleEcho.tensorflow.get_pattern()
            SimpleEcho.stockage.pattern = SimpleEcho.tensorflow.pattern
            
            # Plays audio at scan
            print(SimpleEcho.stockage.pattern)
            audioGetter = AudioGetter(SimpleEcho.stockage.pattern)
            audioFile = audioGetter.get_audio()
            SimpleEcho.audio.play_audio(audioFile)
            led.terminate() """
            
            print(SimpleEcho.stockage.pattern)
        elif sensor == "button18":
            SimpleEcho.buttonRec.action(SimpleEcho.stockage.mode)
            self.send_message(str(SimpleEcho.stockage.pattern))

        # Deletes audio file
        elif sensor == "button4":
            SimpleEcho.buttonDelete.action(SimpleEcho.stockage.mode)
            audioDelete = AudioStoring("", SimpleEcho.stockage.pattern)
            audioDelete.deleteAudio()
            
            print("button4")
        
    def connected(self):
        print(self.address, 'connected')
        SimpleEcho.volumeControl.start()
        
    def handle_close(self):
        print(self.address, 'closed')
        
        
server = WebSocketServer('', 8080, SimpleEcho)
print("server online")
server.serve_forever()

# button = subprocess.Popen(["python", "bouton.py"])
# print("All online")