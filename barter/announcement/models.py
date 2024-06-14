import os

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode

from custom_user.models import CustomUser
from PIL import Image

from utils.storage import NoDuplicatesStorage


class AnnouncementStatuses(models.IntegerChoices): #...
    INACTIVE = 0, 'inactive' # base status
    ACTIVE = 1, 'active' #  status is set after configuration
    ENDED = 2, 'ended' # status is set after funds expire


def announcement_content_upload_to(instance, filename):
    print(instance.__dict__, filename)
    ext = os.path.splitext(filename)[1].lower()
    filename = f'content{ext}'
    path = f'announcement/{instance.pk}/content/{filename}'
    return path

def announcement_preview_upload_to(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    filename = f'preview{ext}'
    return f'announcement/{instance.pk}/preview/{filename}'


def validate_file_size(file):
    max_size = 2 * 1024 * 1024
    if file.size > max_size:
        raise ValidationError(f'Maximum file size mustn\'t exceed 2 mb.')

def validate_files_size(files):
    max_size = 2 * 1024 * 1024
    for file in files:
        if file.size > max_size:
            raise ValidationError(f'Maximum file size mustn\'t exceed 2 mb.')

def validate_image_dimension(image): # file should be sent truncated from the front end
    required_width, required_height = 512, 512
    img = Image.open(image)
    (width, height) = img.size
    if width > required_width or height > required_height:
        raise ValidationError(f'Image mustn\'t be more {required_width}x{required_height} pixels.')
    if width != height:
        raise ValidationError('Image must be square')

def validate_image_extension(file):
    valid_extensions = ['.jpg', '.jpeg', '.png']
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError('Unallowed file extension. Allowed extensions are: .jpg, .jpeg, .png')

def validate_images_extenson(files):
    valid_extensions = ['.jpg', '.jpeg', '.png']
    for file in files:
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in valid_extensions:
            raise ValidationError('Unallowed file extension. Allowed extensions are: .jpg, .jpeg, .png')


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
    preview = models.ImageField(upload_to=announcement_preview_upload_to, validators=[validate_file_size, validate_image_extension],
                                storage=NoDuplicatesStorage(), blank=True, null=True)
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


class AnnouncementMedia(models.Model):
    media = models.ImageField(upload_to=announcement_content_upload_to, validators=[validate_files_size, validate_images_extenson], storage=NoDuplicatesStorage(), blank=True, null=True)
    
    class Meta:
        db_table = 'ann_announcement_media'

class AnnouncementImage(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    media = models.ForeignKey(AnnouncementMedia, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ann_announcement_images'

class Tag(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ann_tag'


class AnnouncementTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ann_announcement_tag'

