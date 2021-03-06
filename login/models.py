from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField()
    intent = models.IntegerField(default=0)
    date_intent = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username
