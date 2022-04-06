import websocket
import time

ws = websocket.create_connection("ws://localhost:8000")

while True:

    ws.send("temp:35.5")
    time.sleep(2)
