from django.db import models
import uuid
from user.models import User
import datetime


class Task(models.Model):
    task_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    priority = models.IntegerField()
    date = models.DateField(default=datetime.date.today)
    text = models.TextField()
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text} by {self.user.username}"
