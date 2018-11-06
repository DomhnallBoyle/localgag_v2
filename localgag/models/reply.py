import uuid
from django.db import models


class Reply(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    comment = models.OneToOneField('Comment')
    status = models.ForeignKey('Status')
    _reply = models.ForeignKey('self', blank=True, null=True)
