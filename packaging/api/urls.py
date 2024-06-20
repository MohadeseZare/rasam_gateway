from django.urls import path

from packaging.api.views import SendDataPackaging, LiveDataPackaging, DailyStaticPackaging, StoppageTimePackaging, \
    LogDataPackaging, ErrorFrequencyPackaging, CumulativeChartPackaging, ErrorListPackaging

urlpatterns = [
    path('sendData/', SendDataPackaging, name='api-send-data'),
    path('liveData/', LiveDataPackaging, name='api-live-data-packaging'),
    path('dailyStatic/', DailyStaticPackaging, name='api-daily-static-report'),
    path('stoppageTime/', StoppageTimePackaging, name='api-stoppage-time-report-packaging'),
    path('logData/', LogDataPackaging, name='api-logData-report-packaging'),
    path('errorFrequency/', ErrorFrequencyPackaging, name='api-error-frequency-report-packaging'),
    path('cumulativeChart/', CumulativeChartPackaging, name='api-Cumulative-chart-report-packaging'),
    path('errorList/', ErrorListPackaging.as_view(), name='api-error-list-packaging'),

]

