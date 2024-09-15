import imaplib
import email
from ..models import Mail
from asyncio import sleep
from ..consumers import WSConsumer
from email.header import decode_header
import base64
from bs4 import BeautifulSoup
import re


class MailBox:
    imap: object

    def __init__(self, settings):
        self.imap = None  # Изначально None
        self.prepare_service(settings)

    @staticmethod
    def get_imap_server_by_email(mail):
        match mail:
            case mail if '@yandex' in mail:
                mail_type = 'imap.yandex.ru'
            case mail if '@gmail' in mail:
                mail_type = 'imap.gmail.ru'
            case _:
                mail_type = 'imap.mail.ru'
        return mail_type

    @staticmethod
    def is_credentials_valid(mail, password):
        imap_server = MailBox.get_imap_server_by_email(mail)
        try:
            imaplib.IMAP4_SSL(imap_server).login(mail, password)
            return True
        except Exception:
            return False

    def prepare_service(self, settings):
        self.imap = imaplib.IMAP4_SSL(settings['imap_server'])
        try:
            self.imap.login(settings['mail'], settings['mail_pass'])
            self.imap.select("INBOX")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            raise MailServiceException('Wrong credentials man:)')


    async def get_messages_uid_list(self):
        status, messages = self.imap.uid('search', "ALL")
        if status == 'OK':
            return messages 
        else:
            return False

    async def start_messages_receiving(self):
        uid_list = get_messages_uids_list()[1]
        for uid in uid_list:
            byte_uid = bytes(str(uid), 'utf-8')  # Преобразование строки в байтовый формат

            res, msg = imap.uid('fetch', byte_uid, '(RFC822)')  # Для метода uid


        new_cons = WSConsumer()
        for el in range(10):
            await sleep(5)
            print('send')
            # await new_cons.websocket_send(text_data=str(el))
        # return messages

    def get_mails_count(self) -> int:
        status, messages = self.imap.select("INBOX")
        # Вернуть количество загруженных сообщений
        return len(messages[0].split())

    @staticmethod
    def add_new_mail(mail_data) -> int:
        new_mail = Mail(mail=email, password=mail_data['password'], type=mail_data['mail_type'],
                        last_message_id=mail_data['last_message_id'])
        new_mail.save()  # Сохранение объекта в БД
        return new_mail.id


class MailServiceException(Exception):
    """Основной класс для исключений MailService."""

    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code
