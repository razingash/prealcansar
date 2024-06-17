from django.urls import path

from .views import *

app_name = 'custom_user'

urlpatterns = [
    path('settings/password/', SettingsPasswordPage.as_view(), name='settings_password'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', RenewedLoginPageView.as_view(), name='password_reset_complete'),
    path('', MainPageView.as_view(), name='main_page'), # MAIN PAGE
    path('login/', LoginPageView.as_view(), name='login'),
    path('register/', RegistrationPageView.as_view(), name='registration'),
    path('logout/', logout_user, name='logout'),
    path('settings/', SettingsPageView.as_view(), name='settings'),
    path('profile/<uuid:profile_uuid>/', ProfileView.as_view(), name='profile'),
]
