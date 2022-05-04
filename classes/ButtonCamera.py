from .Camera import Camera
from .Tensorflow import TensorFlow
from .Audio import Audio
from .AudioGetter import AudioGetter
import subprocess
import time

class ButtonCamera:
    pattern = 0

    def __init__(self, file):
        self.camera = Camera(file)
        self.tensorflow = TensorFlow()
        self.audio = Audio()

    def mode_1(self):
        led = subprocess.Popen(["python", "./led.py"])
        self.camera.take_photo()
        time.sleep(2)
        print("photo")
        self.tensorflow.get_pattern()
        print(self.tensorflow.pattern)

        file = open("./database/sound-volume.txt", "r")
        volume = int(file.readline())

        audioGet = AudioGetter(self.tensorflow.pattern)
        audioFile = audioGet.get_audio()
        self.audio.play_audio(audioFile, volume)
        led.terminate()
        ButtonCamera.pattern = self.tensorflow.pattern

    def action(self, mode):
        if mode == 1:
            self.mode_1()