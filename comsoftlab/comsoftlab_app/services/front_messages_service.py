from asyncio import sleep, get_event_loop


class FrontMessagesService:

    def work(self):
        pass


    @staticmethod
    async def process_message(message, ws):
        loop = get_event_loop()
        match message:
            case message if message == 1:
                for el in range(10):
                    await sleep(5)
                    print('send')
                    await ws.websocket_send(text_data=str(el))
                # mail_service_settings = {
                #     'mail': email,
                #     'mail_pass': password,
                #     'imap_server': MailService.get_imap_server_by_email(email),
                # }
                #
                # mail_service = MailService(mail_service_settings)
                # mail_service.start_messages_receiving()
