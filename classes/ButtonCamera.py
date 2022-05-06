from .Camera import Camera
from .Tensorflow import TensorFlow
from .Audio import Audio
from .AudioGetter import AudioGetter
import subprocess
import time

class ButtonCamera:
    pattern = 0
    volume = 100

    def __init__(self, file):
        self.camera = Camera(file)
        self.tensorflow = TensorFlow()
        self.audio = Audio()

    def mode_1_2(self):
        led = subprocess.Popen(["python", "./led.py"])
        self.camera.take_photo()
        time.sleep(2)
        print("photo")
        self.tensorflow.get_pattern()
        print(self.tensorflow.pattern)

        audioGet = AudioGetter(self.tensorflow.pattern)
        audioFile = audioGet.get_audio()
        self.audio.play_audio(audioFile, ButtonCamera.volume)
        led.terminate()
        ButtonCamera.pattern = self.tensorflow.pattern

    def mode_3(self):
        self.audio.play_audio('./audio/systemAudio/claque.ogg', ButtonCamera.volume)

        led = subprocess.Popen(["python", "./led.py"])
        self.camera.take_photo()
        time.sleep(2)
        print("photo")
        self.tensorflow.get_pattern()
        print(self.tensorflow.pattern)

        audioGet = AudioGetter(self.tensorflow.pattern)
        audioFile = audioGet.get_audio()
        self.audio.play_audio(audioFile, ButtonCamera.volume)
        led.terminate()
        ButtonCamera.pattern = self.tensorflow.pattern

    def action(self, mode):
        file = open("./database/sound-volume.txt", "r")
        #ButtonCamera.volume = int(file.readline())
        print(mode)
        if mode == 1:
            self.mode_1_2()
        elif mode == 2:
            self.mode_1_2()
        elif mode == 3:
            self.mode_3()
            