from channels.consumer import AsyncConsumer
from .services.front_messages_service import FrontMessagesService
import json
from random import randint
from asyncio import sleep
from .models import Mail
from .services.mail_service import MailBox


class WSConsumer(AsyncConsumer):

    def __init__(self):
        pass

    async def websocket_connect(self, event):
        await self.send({"type": "websocket.accept"})

        # try:
        #     # Получаем объект модели Mail по полю mail
        #     mail_obj = Mail.objects.get(mail=mail)
        #     password = mail_obj.password
        #     return password
        # except Mail.DoesNotExist:
        #     # Обработка случая, когда запись с указанным полем mail не найдена
        #     return None

        # email
        # password
        # mail_box = MailBox()

    async def websocket_receive(self, data):
        # Извлечение значения `mail` из принятых данных
        received_date = json.loads(data['text'])
        info = received_date['message']['mail']
        for i in range(10):
                await self.send({
                    "type": "websocket.send",
                    "text": json.dumps(info)
                })
                await sleep(1)
            # await FrontMessagesService.process_message(data['messageType'], self)

    async def websocket_disconnect(self, event):
        pass

    async def websocket_send(self, text_data):
        await self.send({
            "type": "websocket.send",
            "text": text_data
        })
