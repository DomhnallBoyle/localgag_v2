import uuid
from django.db import models


class Location(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    country = models.CharField(max_length=30, default='')
    region = models.CharField(max_length=30, default='')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
