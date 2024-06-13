from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth import get_user_model


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


class ChangeCustomUserForm(forms.ModelForm):
    username = forms.CharField(label='username', widget=forms.TextInput(attrs={'class': 'form_input',
                                                                               'placeholder': 'input username...'}))
    description = forms.CharField(label='contact', widget=forms.Textarea(attrs={'class': 'form_textarea',
                                                                                'placeholder': 'input description...'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'description']

