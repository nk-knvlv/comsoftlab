from django.db import models


# Create your models here.

class Mail(models.Model):
    mail = models.CharField(max_length=255, blank=False)
    password = models.CharField(max_length=255, blank=False)
    type = models.CharField(max_length=255, blank=False)
    last_message_id = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.mail


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(unique=True)  # Уникальный идентификатор сообщения
    subject = models.CharField(max_length=255, blank=False)
    content = models.TextField(blank=False)
    sent_date = models.DateTimeField(blank=False)
    receiving_date = models.DateTimeField(null=True, blank=True)  # Дата получения может не быть
    attached_file_link_list = models.JSONField(default=list)
    mail = models.ForeignKey(Mail, related_name='messages', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Attachment(models.Model):
    message = models.ForeignKey(Message, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/')  # Папка для загрузки файлов
