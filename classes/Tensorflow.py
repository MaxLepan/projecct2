from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import websocket
from ProtocolBuilder import ProtocolBuilder
import time
import rel


# Load the model
class TensorFlow:
    
    def __init__(self):
        self.pattern = 0
        self.model = load_model('./keras_model.h5', compile = False)

    def get_pattern(self):

        # Create the array of the right shape to feed into the keras model
        # The 'length' or number of images you can put into the array is
        # determined by the first position in the shape tuple, in this case 1.
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        # Replace this with the path to your image
        image = Image.open('./img/photo_analyse.png')
        #resize the image to a 224x224 with the same strategy as in TM2:
        #resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

        #turn the image into a numpy array
        image_array = np.asarray(image)
        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        # Load the image into the array
        data[0] = normalized_image_array

        prediction = self.model.predict(data)
        prediction_max = np.argmax(prediction[0])
        self.pattern = prediction_max
        print(self.pattern)

tensorflow = TensorFlow()


def on_message(ws, message):
    print(message)
    if message == "Tensorflow ready":
        tensorflow.get_pattern()
        print(tensorflow.pattern)
        protocol = ProtocolBuilder("Tensorflow", tensorflow.pattern)
        ws.send(protocol.buildProtocol())

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8080",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    print("Tensorflow loaded")

    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
