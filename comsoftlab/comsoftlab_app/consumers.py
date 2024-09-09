from channels.consumer import AsyncConsumer


class YourConsumer(AsyncConsumer):

    def __init__(self):
        pass

    async def websocket_connect(self, event):
        await self.send({"type": "websocket.accept"})

    async def websocket_receive(self, data):
        await self.send({
            "type": "websocket.send",
            "text": f'Hello from Django socket - {data['message']}'
        })

    async def websocket_disconnect(self, event):
        pass

    async def websocket_send(self, text_data):
        await self.send({
            "type": "websocket.send",
            "text": text_data
        })

