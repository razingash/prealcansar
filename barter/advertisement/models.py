from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
from django.utils.text import slugify
from unidecode import unidecode

from custom_user.models import CustomUser

import os
import re

from utils.storage import NoDuplicatesStorage


class CampaingStatuses(models.IntegerChoices):
    INACTIVE = 0, 'inactive' # base status
    ACTIVE = 1, 'active' #  status is set after configuration
    ENDED = 2, 'ended' # status is set after funds expire

class AdvertisementTypes(models.IntegerChoices):
    BANNER = 0, 'banner'
    POPUP = 1, 'pop-up'

def validate_file_extension(file):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.svg']
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(f"Unallowed file extension. Allowed extensions are: {' '.join(valid_extensions)}")

def advertisement_upload_to(instance, filename):
    filename = 'ad' + re.search(r'\.(.*)', filename)[0]
    return f'campaing/{instance.campaing.pk}/advertisements/{instance.pk}/{filename}'

def validate_file_size(value):
    max_size = 2 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError(f'Maximum file size mustn\'t exceed {max_size} bytes.')


class Campaing(models.Model):
    advertiser = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    name = models.CharField(max_length=50, validators=[MinLengthValidator(5)], blank=False, null=False, unique=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    budget = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(10)], default=0,
                                 blank=False, null=False)
    status = models.PositiveSmallIntegerField(choices=CampaingStatuses.choices, default=CampaingStatuses.INACTIVE,
                                              blank=False, null=False)
    campaing_slug = models.SlugField(blank=False, null=True, unique=True)

    def get_absolute_url(self):
        return reverse('campaing', kwargs={'campaing_slug': self.campaing_slug})

    def clean(self):
        if self._state.adding:
            self.campaing_slug = slugify(unidecode(self.name))
            super().clean()
        if self.pk is not None:
            current_campaing = Campaing.objects.only('id', 'status', 'start_date').get(pk=self.pk)
            if self.status != current_campaing.status:
                if current_campaing.status == CampaingStatuses.INACTIVE and self.status == CampaingStatuses.ACTIVE:
                    if self.budget <= Decimal('0'):
                        raise ValidationError('You need more funds.')
                    self.start_date = timezone.now()
                elif self.status == CampaingStatuses.ENDED:
                    self.end_date = timezone.now()
        super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ad_campaings'


class Advertisement(models.Model):
    campaing = models.ForeignKey(Campaing, on_delete=models.PROTECT)
    publication_date = models.DateTimeField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(choices=CampaingStatuses.choices, default=CampaingStatuses.INACTIVE,
                                              blank=False, null=False)
    title = models.CharField(max_length=200,  validators=[MinLengthValidator(10)], blank=False, null=False)
    content = models.TextField(max_length=500, validators=[MinLengthValidator(10)], blank=False, null=False)
    ad_type = models.PositiveSmallIntegerField(choices=AdvertisementTypes.choices, blank=False, null=False)
    file = models.FileField(upload_to=advertisement_upload_to, validators=[validate_file_size, validate_file_extension],
                            storage=NoDuplicatesStorage(), blank=True, null=True)
    title_slug = models.SlugField(blank=False, null=True, unique=True)

    def get_absolute_url(self):
        return reverse('advertisement', kwargs={'title_slug': self.title_slug})

    def clean(self):
        if self._state.adding:
            self.title_slug = slugify(unidecode(self.title))
        super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        if self.pk is None:
            saved_file = self.file
            self.file = None
            super().save(*args, **kwargs)
            self.file = saved_file
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'ad_advertisement'


class ViewStatistic(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.PROTECT)
    watched_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    visitor = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        db_table = 'ad_view_statistic'


class ClickStatistic(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.PROTECT)
    clicked_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    visitor = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        db_table = 'ad_click_statistic'

