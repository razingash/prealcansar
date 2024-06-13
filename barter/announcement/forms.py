
from django import forms
from announcement.models import Announcement


class CreateAnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'description', 'preview', 'content', 'budget', 'title_slug']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form_select'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 4, 'class': 'form_textarea', 'placeholder': 'at least 10 symbols'}),
            'preview': forms.ClearableFileInput(attrs={'class': 'form_image'}),
            'content': forms.ClearableFileInput(attrs={'class': 'form_file'}),
            'budget': forms.NumberInput(attrs={'max': 32767, 'cols': 40, 'rows': 1, 'class': 'form_input'}),
        }


class UpdateAnnouncementForm(forms.ModelForm): # used to update balance and switch status
    class Meta:
        model = Announcement
        fields = ['title', 'status', 'description', 'preview', 'content', 'title_slug']
        widgets = {
            'title': forms.Select(attrs={'class': 'form_select'}),
            'status': forms.Select(attrs={'class': 'form_select'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 4, 'class': 'form_textarea', 'placeholder': 'at least 10 symbols'}),
            'preview': forms.Textarea(attrs={'cols': 60, 'rows': 8, 'class': 'form_textarea', 'placeholder': 'at least 10 symbols'}),
            'content': forms.Select(attrs={'class': 'form_select'}),
        }
