import uuid
from django.db import models


class Comment(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey('User')
    message = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)
