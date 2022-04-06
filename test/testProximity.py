import websocket
import time

ws = websocket.create_connection("ws://localhost:8000")

while True:

    ws.send("Proximity:3456")
    time.sleep(2)
