import imaplib
import email
from ..models import Mail, Message
from asgiref.sync import sync_to_async
import datetime
import quopri
from asyncio import sleep
import base64
from email.header import decode_header
from bs4 import BeautifulSoup


class MailServiceException(Exception):

    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code


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
        try:
            mail_obj = await sync_to_async(lambda: Mail.objects.filter(mail=mail).first())()
            password = mail_obj.password
            return password
        except Message.DoesNotExist:
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
        await sleep(2)
        # await sleep(2)
        if not last_stored:
            data['message_type'] = 2
            await ws.websocket_send(data)
            return uid_list
        else:
            await ws.websocket_send(data)

        # двоичный поиск для оптимизации
        while low < high:
            mid = (low + high) // 2
            if uid_list[mid] <= last_stored:
                data['search_area'][0] = mid + 1
                low = mid + 1
            else:
                data['search_area'][1] = mid
                high = mid

            data['message_type'] = 4
            await ws.websocket_send(data)
            # await sleep(2)
        # После завершения цикла low указывает на первый элемент, который больше last_stored_message_uid
        result_uid = uid_list[low] if low < len(uid_list) else None
        data['message_type'] = 5
        del data['search_area']
        data['result_uid'] = result_uid

        await ws.websocket_send(data)

        return uid_list[low:]

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

    @staticmethod
    async def save_message_into_db(mail, message) -> int:
        new_message = Message(
            uid=message['uid'],
            subject=message['subject'],
            content=message['content'],
            sent_date=datetime.datetime(*message['sent_date'][:6]),
            receiving_date=datetime.datetime(*message['receive_date'][:6]),
            attached_file_link_list=message['attached_file_link_list'],
            mail=mail,
        )
        await sync_to_async(lambda: new_message.save())()  # Сохранение объекта в БД
        return new_message.id

    async def get_new_messages(self, ws, mail):
        # 1 получаем из бд uid последнего сохраненного сообщения
        mail_obj = await sync_to_async(lambda: Mail.objects.filter(mail=mail).first())()
        mail_id = mail_obj.id
        try:
            last_message = await sync_to_async(lambda: Message.objects.filter(mail_id=mail_id).latest('id'))()
            last_message_uid = last_message.uid  # Получаем значение поля uid
        except Message.DoesNotExist:
            last_message_uid = None  # Или выполнить другую логику, например, вернуть сообщение об ошибке
        # 2 далее получаем список uid и определяем индекс первого неполученного сообщения,
        unstored_uid_list = await self.get_unstored_messages_uid_list(ws, last_message_uid)
        await sleep(2)
        # при каждой проверке отправляем это на фронт для визуализации
        # в конце мы должны получить массив неполученных сообщений
        # в котором первый uid будет следующим за последним полученным и до конца

        counter = 0
        for uid in unstored_uid_list:
            message = self.get_message(uid)
            await self.save_message_into_db(mail_obj, message)
            data = {
                'message_type': 6,
                'message': message
            }
            await ws.websocket_send(data)
            counter += 1

    def get_message(self, uid):
        res, msg_obj = self.imap.uid('fetch', str(uid).encode('utf-8'), '(RFC822)')
        msg_obj = email.message_from_bytes(msg_obj[0][1])
        # letter_id = msg_obj["Message-ID"]  # айди письма
        sent_date = email.utils.parsedate_tz(msg_obj["Date"])  # дата получения, приходит >
        receive_date = email.utils.parsedate_tz(msg_obj["Date"])  # дата получения, приходит >

        letter_from = msg_obj["Return-path"]  # e-mail отправителя
        # Объединение и декодирование всех частей
        subject_parts = decode_header(msg_obj["Subject"])
        links = self.get_attachment(msg_obj)
        decoded_subject = ''
        for part, encoding in subject_parts:
            if isinstance(part, bytes):
                # Декодируем строку, если это байты
                if encoding is not None:
                    decoded_subject += part.decode(encoding, errors='replace')
                else:
                    decoded_subject += part.decode('utf-8', errors='replace')  # или другой подходящий
            else:
                # Если это уже строка, просто добавляем её
                decoded_subject += part

        content = self.get_letter_text(msg_obj)
        message = {
            'uid': uid,
            'subject': decoded_subject,
            'sent_date': sent_date,
            'receive_date': receive_date,
            'letter_from': letter_from,
            'content': content,
            'attached_file_link_list': links
        }
        return message

    def get_letter_text(self, msg):
        str_count = 0
        if msg.is_multipart():
            for part in msg.walk():
                if str_count > 5:
                    break
                str_count += 1
                count = 0
                if part.get_content_maintype() == "text" and count == 0:
                    extract_part = self.letter_type(part)
                    if part.get_content_subtype() == "html":
                        letter_text = self.get_letter_text_from_html(extract_part)
                    else:
                        letter_text = extract_part.rstrip().lstrip()
                    count += 1
                    return (
                        letter_text.replace("<", "").replace(">", "").replace("\xa0", " ")
                    )
        else:
            count = 0
            if msg.get_content_maintype() == "text" and count == 0:
                extract_part = self.letter_type(msg)
                if msg.get_content_subtype() == "html":
                    letter_text = self.get_letter_text_from_html(extract_part)
                else:
                    letter_text = extract_part
                count += 1
                return letter_text.replace("<", "").replace(">", "").replace("\xa0", " ")

    @staticmethod
    def letter_type(part):
        if part["Content-Transfer-Encoding"] in (None, "7bit", "8bit", "binary"):
            return part.get_payload()
        elif part["Content-Transfer-Encoding"] == "base64":
            encoding = part.get_content_charset()
            return base64.b64decode(part.get_payload()).decode(encoding)
        elif part["Content-Transfer-Encoding"] == "quoted-printable":
            encoding = part.get_content_charset()
            return quopri.decodestring(part.get_payload()).decode(encoding)
        else:  # all possible types: quoted-printable, base64, 7bit, 8bit, and binary
            return part.get_payload()

    @staticmethod
    def get_letter_text_from_html(body):
        body = body.replace("<div><div>", "<div>").replace("</div></div>", "</div>")
        try:
            soup = BeautifulSoup(body, "html.parser")
            paragraphs = soup.find_all("div")
            text = ""
            for paragraph in paragraphs:
                text += paragraph.text + "\n"
            return text.replace("\xa0", " ")
        except (Exception) as exp:
            print("text ftom html err ", exp)
            return False

    def get_attachment(self, msg):
        attachments_links = []
        for part in msg.walk():
            if part.get_content_disposition() == "attachment":
                filename = part.get_filename()
                filename = self.from_subj_decode(filename)
                attachments_links.append(filename)
        return attachments_links

    @staticmethod
    def from_subj_decode(msg_from_subj):
        if msg_from_subj:
            encoding = decode_header(msg_from_subj)[0][1]
            msg_from_subj = decode_header(msg_from_subj)[0][0]
            if isinstance(msg_from_subj, bytes):
                msg_from_subj = msg_from_subj.decode(encoding)
            if isinstance(msg_from_subj, str):
                pass
            msg_from_subj = str(msg_from_subj).strip("<>").replace("<", "")
            return msg_from_subj
        else:
            return None
