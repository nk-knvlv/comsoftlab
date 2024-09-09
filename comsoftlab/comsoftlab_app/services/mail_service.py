import imaplib
import email
from email.header import decode_header
import base64
from bs4 import BeautifulSoup
import re


class MailService:
    imap: object

    def __init__(self, request, settings):
        self.prepare_service(request, settings)

    def prepare_service(self, request, settings):
        self.imap = imaplib.IMAP4_SSL(settings['imap_server'])
        try:
            self.imap.login(request.user.username, settings['mail_pass'])
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    def get_mails(self):
        status, messages = self.imap.uid('search', "ALL")
        pass

    def get_messages_count(self) -> int:
        status, messages = self.imap.select("INBOX")
        # Вернуть количество загруженных сообщений
        return len(messages[0].split())
