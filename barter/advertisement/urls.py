from django.urls import path

from .views import *

app_name = 'advertisement'

urlpatterns = [
    path('campaing/', CreateCampaingPageView.as_view(), name='create_campaing'),
    path('campaing/<slug:campaing_slug>/', CampaingPageView.as_view(), name='campaing'),
    path('campaing/update/<slug:campaing_slug>/', UpdateCampaingPageView.as_view(), name='update_campaing'),
    path('advertisement/', CreateAdvertisementPageView.as_view(), name='create_advertisement'),
    path('advertisement/<slug:title_slug>/', AdvertisementPageView.as_view(), name='advertisement'),
    path('advertisement/update/<slug:title_slug>/', UpdateAdvertisementPageView.as_view(), name='update_advertisement'),
]
