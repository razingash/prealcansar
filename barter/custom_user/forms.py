from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth import get_user_model


class RegisterAdvertiserForm(UserCreationForm):
    username = forms.CharField(label='username', widget=forms.TextInput(attrs={'class': 'input_username', 'placeholder': 'input username...'}))
    email = forms.EmailField(label='email', widget=forms.EmailInput(attrs={'class': 'input_mail', 'placeholder': 'input email...'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'input_password', 'placeholder': 'input password...'}))
    password2 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'input_password', 'placeholder': 'repeat password...'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']


class LoginCustomUserForm(AuthenticationForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'input_password',
                                                                                   'placeholder': 'input password...'}))
    username = forms.CharField(label='username', widget=forms.TextInput(attrs={'class': 'input_username',
                                                                               'placeholder': 'input username...'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class ChangeCustomUserForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'input_password',
                                                                                   'placeholder': 'input password...'}))
    username = forms.CharField(label='username', widget=forms.TextInput(attrs={'class': 'input_username',
                                                                               'placeholder': 'input username...'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'contact']

