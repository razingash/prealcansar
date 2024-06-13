from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


# Create your models here.

class CustomUser(AbstractUser):
    uuid = models.UUIDField(primary_key=False, default=uuid4, editable=False, unique=True)
    description = models.TextField(max_length=1000, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'profile_uuid': self.uuid})

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'ad_advertiser'
