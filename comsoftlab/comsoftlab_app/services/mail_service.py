import imaplib
import email
from ..models import Mail, Message
from asgiref.sync import sync_to_async
from django.db import models
import bisect
from asyncio import sleep
import base64
from email.header import decode_header
from bs4 import BeautifulSoup
import re


class MailBox:
    imap: object

    def __init__(self, mail):
        self.imap = None  # Изначально None
        self.mail = mail

    async def async_init(self):
        await self.prepare_service(self.mail)

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
    async def _get_mail_pass(mail):
        print('_get_mail_pass')
        try:
            print('пиздец')
            print(mail)
            mail_obj = await sync_to_async(lambda: Mail.objects.filter(mail=mail).first())()
            password = mail_obj.password
            print('это мыло', mail)
            return password
        except Message.DoesNotExist:
            print('нету')
            return None

    @staticmethod
    def is_credentials_valid(mail, password):
        imap_server = MailBox.get_imap_server_by_email(mail)
        try:
            imaplib.IMAP4_SSL(imap_server).login(mail, password)
            return True
        except Exception:
            return False

    async def prepare_service(self, mail):
        try:
            mail_server = self.get_imap_server_by_email(mail)
            mail_password = await self._get_mail_pass(mail)

            self.imap = imaplib.IMAP4_SSL(mail_server)
            self.imap.login(mail, mail_password)
            self.imap.select("INBOX")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            raise MailServiceException('Wrong credentials man:)')

    def get_messages_uid_list(self):
        status, byte_uid_list = self.imap.uid('search', "ALL")
        if status != 'OK':
            return []

        return [int(id_str) for id_str in byte_uid_list[0].decode('utf-8').split(' ')]

    async def get_unstored_messages_uid_list(self, ws, last_stored):
        uid_list = self.get_messages_uid_list()

        if not uid_list:
            raise MailServiceException(message='Imap lib trouble')

        low = 0
        high = len(uid_list)
        search_area = [low, high]
        # отправляем первоначальные данные для визуализации поиска на фронт
        data = {
            'message_type': 3,
            'search_area': search_area,
        }

        if not last_stored:
            data['message_type'] = 2
            await ws.websocket_send(data)
            return uid_list

        await ws.websocket_send(data)

        # двоичный поиск для оптимизации
        while low < high:
            mid = (low + high) // 2
            print('mid', mid)
            print('uid_list[mid]', uid_list[mid])
            if uid_list[mid] <= last_stored:
                data['search_area'][0] = mid + 1
                low = mid + 1
            else:
                data['search_area'][1] = mid
                high = mid

            await ws.websocket_send(data)

        # После завершения цикла low указывает на первый элемент, который больше last_stored_message_uid
        result_uid = uid_list[low] if low < len(uid_list) else None
        data['message_type'] = 4
        data['result_uid'] = result_uid

        await ws.websocket_send(data)

        return result_uid

    async def get_new_messages(self, ws, mail):
        # 1 получаем из бд uid последнего сохраненного сообщения
        try:
            mail_obj = await sync_to_async(lambda: Mail.objects.filter(mail=mail).first())()
            mail_id = mail_obj.id
            last_message = await sync_to_async(lambda: Message.objects.filter(mail_id=mail_id).latest('id'))()
            last_message_uid = last_message.uid  # Получаем значение поля uid
        except Message.DoesNotExist:
            last_message_uid = None  # Или выполнить другую логику, например, вернуть сообщение об ошибке
        # 2 далее получаем список uid и определяем индекс первого неполученного сообщения,
        uid_list = await self.get_unstored_messages_uid_list(ws, last_message_uid)

        # при каждой проверке отправляем это на фронт для визуализации
        # в конце мы должны получить массив неполученных сообщений
        # в котором первый uid будет следующим за последним полученным и до конца

        # далее после
        # await MailBox.get_message_receiver()

        # получение новых сообщений

        # далее создаем генератор, который будет получать
        # message отправлять его на фронт и в бд (пока по одному далее по 5)
        # когда генератор подходит к концу он еще раз запращивает uids, вдруг есть какие-то новые,
        # если новых нет отправляет сигнал конца

        # тут я должен знать email типа и проследить я это должен от вызова
        last_stored_message_uid = '227'
        # uid_list = self.get_messages_uid_list()
        # чтобы получить пароль
        # Mail.objects.filter(mail=email)

    #
    # async def get_message_receiver(self):
    #     for uid in uid_list:
    #         byte_uid = bytes(str(uid), 'utf-8')  # Преобразование строки в байтовый формат
    #
    #         res, msg = self.imap.uid('fetch', byte_uid, '(RFC822)')  # Для метода uid

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

    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code
