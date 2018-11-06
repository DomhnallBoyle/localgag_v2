import uuid
from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(User):
    """
    number: Mobile number for confirmation purposes
    radius: Radius of area to post/search in (km)
    location: Information about the user's current location
    """
    # number = PhoneNumberField()
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=5, default='')
    radius = models.IntegerField(default=5)
    location = models.OneToOneField('Location')

    @property
    def latitude(self):
        return self.location.latitude

    @property
    def longitude(self):
        return self.location.longitude

    @property
    def to_dict(self):
        return {'username': self.username, 'password': self.password}
