
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode

from custom_user.models import CustomUser
import re


class AnnouncementStatuses(models.IntegerChoices): #...
    INACTIVE = 0, 'inactive' # base status
    ACTIVE = 1, 'active' #  status is set after configuration
    ENDED = 2, 'ended' # status is set after funds expire

def validate_file_extension(value):
    pass

def announcement_content_upload_to(instance, filename):
    print(instance, instance.__dict__)
    filename = 'ann' + re.search(r'\.(.*)', filename)[0]
    return f'announcement/{instance.pk}/content/{filename}'

def announcement_preview_upload_to(instance, filename):
    print(instance, instance.__dict__)
    filename = 'ann' + re.search(r'\.(.*)', filename)[0]
    return f'advertisements/{instance.pk}/preview/{filename}'

def validate_file_size(value):
    max_size = 2 * 512 * 512
    if value.size > max_size:
        raise ValidationError(f'Maximum file size mustn\'t exceed {max_size} bytes.')


class Announcement(models.Model):
    announcer = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    publication_starts = models.DateTimeField(blank=True, null=True)
    publication_ends = models.DateTimeField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(choices=AnnouncementStatuses.choices, default=AnnouncementStatuses.INACTIVE,
                                              blank=False, null=False)
    budget = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(10)], default=0,
                                 blank=False, null=False)
    title = models.CharField(max_length=300, blank=False, null=False, validators=[MinLengthValidator(15)])
    description = models.TextField(max_length=5000, blank=False, null=False, validators=[MinLengthValidator(15)])
    preview = models.ImageField(upload_to=announcement_preview_upload_to, validators=[validate_file_size], blank=True, null=True)
    content = models.FileField(upload_to=announcement_content_upload_to, validators=[validate_file_size, validate_file_extension],
                               blank=True, null=True)
    title_slug = models.SlugField(blank=False, null=True, unique=True)

    def get_absolute_url(self):
        return reverse('announcement', kwargs={'title_slug': self.title_slug})

    def clean(self):
        if self._state.adding:
            self.title_slug = slugify(unidecode(self.title))
            super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'ann_announcement'


class Tag(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ann_tag'


class AnnouncementTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE) # ?
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ann_announcement_tag'

