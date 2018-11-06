import uuid
from django.db import models


class Status(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    comment = models.OneToOneField('Comment')
    location = models.OneToOneField('Location')
    media_filename = models.CharField(max_length=50)

    @property
    def latitude(self):
        return self.location.latitude

    @property
    def longitude(self):
        return self.location.longitude
