from asgiref.sync import sync_to_async
from asyncio import sleep, get_event_loop
from .mail_service import MailBox


class FrontMessagesService:

    @staticmethod
    async def process_message(message, ws):
        message_type = message['messageType']
        mail = message['mail']
        match message_type:
            case message_type if message_type == 1:
                mailbox = MailBox(mail)
                await mailbox.async_init()
                await mailbox.get_new_messages(ws, mail)
