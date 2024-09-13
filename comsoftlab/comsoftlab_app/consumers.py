from channels.consumer import AsyncConsumer
from .services.front_messages_service import FrontMessagesService
import json


class YourConsumer(AsyncConsumer):

    def __init__(self):
        pass

    async def websocket_connect(self, event):
        await self.send({"type": "websocket.accept"})

    async def websocket_receive(self, data):
        await self.send({
            "type": "websocket.send",
            "text": data
        })
        # await FrontMessagesService.process_message(data['messageType'], self)

    async def websocket_disconnect(self, event):
        pass

    async def websocket_send(self, text_data):
        await self.send({
            "type": "websocket.send",
            "text": text_data
        })
