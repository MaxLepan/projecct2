import websocket

ws = websocket.create_connection("ws://localhost:8000")

ws.send("button:HIGH")

