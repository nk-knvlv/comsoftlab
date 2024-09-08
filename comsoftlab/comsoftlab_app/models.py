from django.db import models


# Create your models here.

class Message(models.Model):
    message_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255, blank=False)
    text = models.TextField(blank=False)
    sent_date = models.DateTimeField(blank=False)
    receiving_date = models.DateTimeField(blank=False)

    # files_list = тут пока не понятно TODO
    def __str__(self):
        return self.title
