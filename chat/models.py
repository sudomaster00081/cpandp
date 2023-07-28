# models.py

from django.db import models
from django.utils import timezone

class Room(models.Model):
    room_id = models.CharField(max_length=10, unique=True)
    room_name = models.CharField(max_length=100)
    description = models.TextField()
    time_limit = models.DurationField(default=timezone.timedelta(hours=1))
    passkey = models.CharField(max_length=50, blank=True, null=True)  # Optional passkey for authentication

    def __str__(self):
        return self.room_name

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender}: {self.content}"
