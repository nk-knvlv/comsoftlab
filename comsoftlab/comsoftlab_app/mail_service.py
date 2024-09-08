import imaplib
import email
from email.header import decode_header
import base64
from bs4 import BeautifulSoup
import re


mail_pass = "MPenUT0nfBBfsduvzvHB"
username = "obande@mail.ru"
imap_server = "imap.mail.ru"
imap = imaplib.IMAP4_SSL(imap_server)
print(imap.login(username, mail_pass))
print(imap.select("INBOX"))
# Получение ID всех писем
status, messages = imap.search(None, 'ALL')

# Вернуть количество загруженных сообщений
print(f'Total messages retrieved: {len(messages[0].split())}')


