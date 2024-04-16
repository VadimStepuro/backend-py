from starlette.websockets import WebSocket


class ConnectionManger:
    def __init__(self) -> None:
        self.connection = []

    def add(self, connection: WebSocket):
        self.connection.append(connection)

    async def remove(self, websocket: WebSocket):
        if websocket in self.connection:
            self.connection.remove(websocket)
            await websocket.close()

    async def broadcast(self, type, data):
        for i in self.connection:
            await i.send_json({
                "message": {
                    "type": type,
                    "data": data
                }
            })
