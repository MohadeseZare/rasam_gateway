from django.contrib import admin
from .models import PackagingLlogData, PackagingLiveData, TypeOfAlarm,  Alarm, AggregateData

admin.site.register(PackagingLlogData)
admin.site.register(PackagingLiveData)
admin.site.register(TypeOfAlarm)
admin.site.register(Alarm)
admin.site.register(AggregateData)

