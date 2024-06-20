from django.urls import path, include
from .views import *
from .viewslogReports import logsInPeriodAggre, logsInPeriodData
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('livedata', LiveDataViewSet, basename='livedata')
router.register('logdata', LogDataViewSet, basename='logdata')

urlpatterns = [
    path('gateway/', include(router.urls)),
    path('gateway/api/add_data/', add_data),
    path('gateway/api/getLogs/inPeriod/', logsInPeriodAggre),
    path('gateway/get-charges-as-date/', get_charges_in_time_range),
    # path('gateway/api/getLogs/chargecounts/get_charges_by_date_and_status/', get_charges_by_date_and_status),
    path('gateway/api/add_data/offline/', offline_data),
    path('gateway/api/add_data/test/', test),
    path('gateway/get_charges_as_date_and_status/', get_charges_in_time_range_as_date_status)
]