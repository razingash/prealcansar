
from django import forms
from advertisement.models import Campaing, Advertisement


class CreateCampaingForm(forms.ModelForm):
    class Meta:
        model = Campaing
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form_input', 'placeholder': 'at least 10 symbols'})
        }


class UpdateCampaingForm(forms.ModelForm): # used to update balance and switch status
    class Meta:
        model = Campaing
        fields = ['budget', 'status']
        widgets = {
            'budget': forms.NumberInput(attrs={'max': 32767, 'cols': 40, 'rows': 1, 'class': 'form_input'}),
            'status': forms.Select(attrs={'class': 'form_select'})
        }


class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['campaing', 'title', 'content', 'ad_type', 'file']
        widgets = {
            'campaing': forms.Select(attrs={'class': 'form_select'}),
            'title': forms.Textarea(attrs={'cols': 60, 'rows': 4, 'class': 'form_textarea', 'placeholder': 'at least 10 symbols'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 8, 'class': 'form_textarea', 'placeholder': 'at least 10 symbols'}),
            'ad_type': forms.Select(attrs={'class': 'form_select'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form_file'})
        }
