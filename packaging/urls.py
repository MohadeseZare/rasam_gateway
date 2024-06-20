from django.urls import path

from packaging.api.views import SendDataPackaging, LiveDataPackaging

urlpatterns = [
    path('sendData/', SendDataPackaging, name='api-send-data'),
    path('liveData/', LiveDataPackaging.as_view(), name='api-live-data-packaging'),
]

