import websocket

ws = websocket.create_connection("ws://localhost:8080")

ws.send("button17:HIGH")

