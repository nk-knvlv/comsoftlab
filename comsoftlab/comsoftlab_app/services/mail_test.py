import imaplib
import email
from email.header import decode_header
import base64
from bs4 import BeautifulSoup
import re
from pprint import pprint

mail_pass = "MPenUT0nfBBfsduvzvHB"
username = "obande@mail.ru"
imap_server = "imap.mail.ru"
imap = imaplib.IMAP4_SSL(imap_server)
result = imap.login(username, mail_pass)
print(result)
imap.select("INBOX")


def get_uid_list():
    try:
        status, messages = imap.uid('search', None, "ALL")
        if status == "OK":
            return messages
        else:
            return False
    except Exception as e:
        print(f'there is error {e}')

    # print(get_uid_list())


def get_message_receiver(last_stored_message_uid):
    try:
        uid_list = get_uid_list()
    except Exception as e:
        print(f'there is error {e}')
    if uid_list:
        for i in range(1, 5):
            yield i


#

# result = get_message_receiver()
# print(next(result))
# print(next(result))
# uid_list = get_uid_list()
res, msg = imap.uid('fetch', b'227', '(RFC822)')  #Для метода uid
# fst_unstored_msg_uid = uid_list(uid_list.index(last_stored_message_uid) + 1)
# message_list = {}
# for _ in uid_list
print(res)
pprint(msg)
# [last_stored_message_uid
