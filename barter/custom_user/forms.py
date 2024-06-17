from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordResetForm
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from custom_user.models import CustomUser


class RegisterCustomUserForm(UserCreationForm):
    username = forms.CharField(label='username', widget=forms.TextInput(attrs={'class': 'form_input', 'placeholder': 'input username...'}))
    email = forms.EmailField(label='email', widget=forms.EmailInput(attrs={'class': 'form_email_input', 'placeholder': 'input email...'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form_password', 'placeholder': 'input password...'}))
    password2 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form_password', 'placeholder': 'repeat password...'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']


class LoginCustomUserForm(AuthenticationForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form_password',
                                                                                   'placeholder': 'input password...'}))
    username = forms.CharField(label='username', widget=forms.TextInput(attrs={'class': 'form_input',
                                                                               'placeholder': 'input username...'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={"autocomplete": "email", 'class': 'form_input', 'placeholder': 'input email...'}))


class CustomPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'form_input', 'placeholder': 'input password...'}))
    new_password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(attrs={'class': 'form_input', 'placeholder': 'repeat password...'}))


class ChangeCustomUserPasswordForm(SetPasswordForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'class': 'form_input'}))
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'form_input'}))
    new_password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(attrs={'class': 'form_input'}))

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        if new_password1 != new_password2:
            raise forms.ValidationError("The two password fields didn't match1.")
        user = self.user
        if not user.check_password(old_password):
            raise forms.ValidationError("Your old password was entered incorrectly.")
        return cleaned_data

    class Meta:
        model = get_user_model()
        fields = ['old_password', 'new_password1', 'new_password2']
        widgets = {
            'old_password': forms.PasswordInput(attrs={'class': 'form_input'}),
            'new_password1': forms.PasswordInput(attrs={'class': 'form_input'}),
            'new_password2': forms.PasswordInput(attrs={'class': 'form_input'})
        }



class ChangeCustomUserForm(forms.ModelForm):
    username = forms.CharField(label='username', widget=forms.TextInput(attrs={'class': 'form_input',
                                                                               'placeholder': 'input username...'}))
    description = forms.CharField(label='contact', widget=forms.Textarea(attrs={'class': 'form_textarea',
                                                                                'placeholder': 'input description...'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'description']

