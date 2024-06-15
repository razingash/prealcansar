
from django import forms
from django.core.exceptions import ValidationError

from announcement.models import Announcement, AnnouncementMedia, AnnouncementImage


class MultipleFileInput(forms.ClearableFileInput):
    """circus, in previous versions ClearableFileInput supported 'multiple': True"""
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, max_files=None, max_size=None, **kwargs):
        self.max_files = max_files
        self.max_size = max_size
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None): # clean for media field
        print(data)
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            if self.max_files and len(data) > self.max_files:
                raise ValidationError(f"You can't upload more than {self.max_files} images")
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class CreateAnnouncementImagesForm(forms.ModelForm):
    media = MultipleFileField(max_files=3, required=False)
    #media = forms.ImageField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}))

    class Meta:
        model = AnnouncementMedia
        fields = ['media']


class UpdateAnnouncementImagesForm(forms.ModelForm):
    media = MultipleFileField(max_files=3, required=False)

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance:
            initial_media = AnnouncementImage.objects.filter(announcement=instance)
            print(initial_media)
            kwargs.update(initial={
                'media': initial_media,
            })
        super().__init__(*args, **kwargs)

    class Meta:
        model = AnnouncementMedia
        fields = ['media']


class CreateAnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'description', 'preview', 'budget']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form_select'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 4, 'class': 'form_textarea', 'placeholder': 'at least 10 symbols'}),
            'preview': forms.ClearableFileInput(attrs={'class': 'form_image'}),
            'budget': forms.NumberInput(attrs={'max': 32767, 'cols': 40, 'rows': 1, 'class': 'form_input'}),
        }


class UpdateAnnouncementForm(forms.ModelForm): # used to update balance and switch status
    class Meta:
        model = Announcement
        fields = ['title', 'description', 'preview']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form_select'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 4, 'class': 'form_textarea', 'placeholder': 'at least 10 symbols'}),
            'preview': forms.ClearableFileInput(attrs={'class': 'form_image'}),
        }
