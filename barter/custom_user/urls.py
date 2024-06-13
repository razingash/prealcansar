from django.contrib.sitemaps.views import sitemap
from django.urls import path

from .views import *

urlpatterns = [
    path('login/', LoginPageView.as_view(), name='login'),
    path('register/', RegistrationPageView.as_view(), name='registration'),
    path('logout/', logout_user, name='logout'),
    path('settings/', SettingsPageView.as_view(), name='settings'),
    path('profile/<uuid:profile_uuid>/', ProfileView.as_view(), name='profile'),
]
