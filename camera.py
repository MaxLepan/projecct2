from picamera import PiCamera
import time

camera = PiCamera()


class Camera:
    
    def __init__ (self, name):
        self.name = name
    
    def take_photo(self):
        camera.start_preview()
        time.sleep(2)
        camera.capture(self.name)
        camera.stop_preview()