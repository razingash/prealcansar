from django.urls import path

from .views import *

urlpatterns = [
    path('announcement/', CreateAnnouncementPageView.as_view(), name='create_announcement'),
    path('announcement/<slug:title_slug>/', AnnouncementPageView.as_view(), name='announcement'),
    path('announcement/update/<slug:title_slug>/', UpdateAnnouncementPageView.as_view(), name='update_announcement'),
]
