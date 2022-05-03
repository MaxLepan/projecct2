import websocket

ws = websocket.create_connection("ws://localhost:8000")

ws.send("mode:TUTORIAL")
#ws.send("mode:INTERMEDIATE")
#ws.send("mode:EXPERT")
