import websocket
import time

ws = websocket.create_connection("ws://localhost:8000")

while True:

    ws.send("prox:3456")
    time.sleep(2)
