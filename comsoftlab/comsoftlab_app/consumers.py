from channels.consumer import AsyncConsumer
from .services.front_messages_service import FrontMessagesService
import json
from random import randint
from asyncio import sleep


class WSConsumer(AsyncConsumer):

    def __init__(self):
        pass

    async def websocket_connect(self, event):
        await self.send({"type": "websocket.accept"})
        for i in range(10):
            print('send')
            data = json.dumps({'message': randint(1, 100)})
            await self.send({
                "type": "websocket.send",
                "text": data
            })
            await sleep(1)

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
